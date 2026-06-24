import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.llm.agents.base import BaseAgent
from src.llm.handlers.content.slide_agents import MediaAgent
from src.schemas.agent_protocol import AgentTask, AgentTaskResult
from src.tools.bootstrap import get_mcp_client

logger = logging.getLogger("chatbot.agents.media_research")

_MAX_MEDIA_LOOKUPS = 4
_MEDIA_LOOKUP_WORKERS = 4
_ALLOWED_MEDIA_TYPES = {"image", "gif", "animation", "diagram", "infographic"}


class MediaResearchAgent(BaseAgent):
    agent_id = "media_research_agent"
    default_error_code = "MEDIA_AGENT_ERROR"

    def _run(self, task: AgentTask) -> AgentTaskResult:
        inputs = task.inputs
        agent = MediaAgent()
        result = agent.run(
            topic=inputs.get("topic", ""),
            grade=inputs.get("grade", ""),
            book=inputs.get("book", ""),
            outline_payload=inputs.get("outline_payload") or {},
            content_payload=inputs.get("content_payload") or {},
        )
        payload = result.payload or {}
        used_tools = ["llm_generation"]

        if result.status == "success" and self._enrich_media_urls(
            payload,
            topic=inputs.get("topic", ""),
            grade=inputs.get("grade", ""),
            book=inputs.get("book", ""),
        ):
            used_tools.append("web_search")

        return AgentTaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status=result.status,
            artifact_type=task.expected_artifact or "media_payload",
            artifact=payload,
            confidence=0.75 if result.status == "success" else None,
            used_tools=used_tools,
            latency_ms=result.latency_ms,
            error_code=result.error_code,
            error_message=result.error_message,
        )

    def _enrich_media_urls(self, payload: dict, *, topic, grade, book) -> bool:
        items = (payload.get("inline_media") or []) + (payload.get("hero_media") or [])
        items = [
            item for item in items
            if not item.get("url") and self._should_lookup_item(item)
        ][:_MAX_MEDIA_LOOKUPS]
        if not items:
            return False

        client = get_mcp_client()
        results = []
        with ThreadPoolExecutor(max_workers=min(_MEDIA_LOOKUP_WORKERS, len(items))) as executor:
            futures = [
                executor.submit(
                    self._enrich_single_item,
                    item,
                    client=client,
                    topic=topic,
                    grade=grade,
                    book=book,
                )
                for item in items
            ]
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as exc:
                    logger.warning(
                        "Media enrich worker failed | error=%s",
                        str(exc)[:160],
                    )
                    results.append(False)
        return any(results)

    def _enrich_single_item(self, item: dict, *, client, topic, grade, book) -> bool:
        query = (
            item.get("query")
            or item.get("caption")
            or item.get("description")
            or topic
            or ""
        ).strip()
        if not query:
            return False

        requested_type = item.get("type") or "image"
        media_type = (
            requested_type
            if requested_type in _ALLOWED_MEDIA_TYPES
            else "image"
        )
        item["type"] = media_type
        try:
            response = client.search_media(
                query=query,
                topic=topic,
                grade=grade,
                book=book,
                media_types=[media_type],
                top_k=3,
            )
        except Exception as exc:
            logger.warning(
                "MCP media lookup failed | type=%s query=%s error=%s",
                media_type,
                query[:80],
                str(exc)[:160],
            )
            return False

        if not response.success or not response.data:
            return False

        media_items = response.data.get("media_items") or []
        picked = next(
            (
                media
                for media in media_items
                if media.get("media_type") == media_type
            ),
            media_items[0] if media_items else None,
        )
        if not picked or not picked.get("url"):
            return False

        item["url"] = picked["url"]
        item["media_type"] = picked.get("media_type", media_type)
        if not item.get("source_url"):
            item["source_url"] = picked.get("source_url", "")
        if not item.get("source_title"):
            item["source_title"] = picked.get("source_title", "")
        if picked.get("relevance_score") is not None:
            item["relevance_score"] = picked["relevance_score"]
        return True

    @staticmethod
    def _should_lookup_item(item: dict) -> bool:
        slide_type = str(item.get("for_slide_type") or "").lower()
        if slide_type in {"exercise", "summary", "agenda", "section"}:
            return False
        return True


__all__ = ["MediaResearchAgent"]
