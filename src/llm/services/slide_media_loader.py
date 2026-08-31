from __future__ import annotations

import ipaddress
import logging
import socket
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

import httpx

from src.config.config import settings


logger = logging.getLogger("chatbot.slide_media_loader")


class SlideMediaLoader:
    def __init__(self):
        self.cache: Dict[str, Optional[bytes]] = {}

    def clear(self) -> None:
        self.cache.clear()

    def download(self, url: str) -> Optional[bytes]:
        if url in self.cache:
            return self.cache[url]
        if not self.is_public_url(url):
            logger.warning("Blocked non-public media URL")
            self.cache[url] = None
            return None

        current_url = url
        try:
            with httpx.Client(
                timeout=settings.MEDIA_DOWNLOAD_TIMEOUT_SECONDS,
                follow_redirects=False,
            ) as client:
                for _ in range(3):
                    response = client.get(current_url)
                    if response.is_redirect:
                        location = response.headers.get("location")
                        if not location:
                            break
                        current_url = urljoin(current_url, location)
                        if not self.is_public_url(current_url):
                            break
                        continue
                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "").lower()
                    content = response.content
                    if not content_type.startswith("image/"):
                        break
                    if len(content) > settings.MEDIA_DOWNLOAD_MAX_BYTES:
                        break
                    self.cache[url] = content
                    return content
        except Exception as exc:
            logger.warning("Media download failed | error=%s", str(exc)[:160])

        self.cache[url] = None
        return None

    @staticmethod
    def is_public_url(url: str) -> bool:
        try:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname:
                return False
            addresses = {
                item[4][0]
                for item in socket.getaddrinfo(parsed.hostname, parsed.port or 443)
            }
            if not addresses:
                return False
            return all(SlideMediaLoader._is_public_address(address) for address in addresses)
        except (OSError, ValueError):
            return False

    @staticmethod
    def _is_public_address(address: str) -> bool:
        ip = ipaddress.ip_address(address)
        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        )


__all__ = ["SlideMediaLoader"]
