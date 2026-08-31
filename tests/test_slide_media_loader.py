from types import SimpleNamespace

import pytest

from src.llm.services import slide_media_loader
from src.llm.services.slide_media_loader import SlideMediaLoader


class FakeResponse:
    def __init__(self, *, content=b"image", content_type="image/png", redirect=None):
        self.content = content
        self.headers = {"content-type": content_type}
        if redirect:
            self.headers["location"] = redirect
        self.is_redirect = redirect is not None

    def raise_for_status(self):
        return None


class FakeClient:
    def __init__(self, responses, calls, **kwargs):
        self.responses = iter(responses)
        self.calls = calls

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def get(self, url):
        self.calls.append(url)
        return next(self.responses)


def _install_client(monkeypatch, responses):
    calls = []
    monkeypatch.setattr(
        slide_media_loader.httpx,
        "Client",
        lambda **kwargs: FakeClient(responses, calls, **kwargs),
    )
    return calls


def test_media_loader_caches_successful_download(monkeypatch):
    calls = _install_client(monkeypatch, [FakeResponse(content=b"png")])
    monkeypatch.setattr(SlideMediaLoader, "is_public_url", staticmethod(lambda url: True))
    loader = SlideMediaLoader()

    assert loader.download("https://example.edu/image.png") == b"png"
    assert loader.download("https://example.edu/image.png") == b"png"
    assert calls == ["https://example.edu/image.png"]


@pytest.mark.parametrize(
    ("response", "max_bytes"),
    [
        (FakeResponse(content_type="text/html"), 1024),
        (FakeResponse(content=b"too-large"), 2),
    ],
)
def test_media_loader_rejects_invalid_type_and_oversize(
    monkeypatch, response, max_bytes
):
    _install_client(monkeypatch, [response])
    monkeypatch.setattr(SlideMediaLoader, "is_public_url", staticmethod(lambda url: True))
    monkeypatch.setattr(
        slide_media_loader,
        "settings",
        SimpleNamespace(MEDIA_DOWNLOAD_TIMEOUT_SECONDS=1, MEDIA_DOWNLOAD_MAX_BYTES=max_bytes),
    )

    assert SlideMediaLoader().download("https://example.edu/file") is None


def test_media_loader_blocks_redirect_to_private_network(monkeypatch):
    calls = _install_client(
        monkeypatch,
        [FakeResponse(redirect="http://127.0.0.1/private.png")],
    )
    monkeypatch.setattr(
        SlideMediaLoader,
        "is_public_url",
        staticmethod(lambda url: "127.0.0.1" not in url),
    )

    assert SlideMediaLoader().download("https://example.edu/image.png") is None
    assert calls == ["https://example.edu/image.png"]


def test_media_loader_rejects_non_public_ip_classes():
    for address in ("127.0.0.1", "10.0.0.1", "169.254.1.1", "224.0.0.1"):
        assert SlideMediaLoader._is_public_address(address) is False
    assert SlideMediaLoader._is_public_address("8.8.8.8") is True
