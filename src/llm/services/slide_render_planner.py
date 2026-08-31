from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from src.llm.services.slide_render_models import RenderPlan, RenderSlideModel


RICH_LAYOUTS = {
    "code": "EDU_CODE",
    "table": "EDU_TABLE",
    "chart": "EDU_CHART",
    "process": "EDU_PROCESS",
    "comparison": "EDU_COMPARISON",
}


class SlideRenderPlanner:
    """Convert logical generated slides into deterministic physical slides."""

    def plan(self, raw_slides: List[Dict[str, Any]]) -> RenderPlan:
        planned: List[RenderSlideModel] = []
        answers: List[Dict[str, Any]] = []
        warnings: List[str] = []
        question_number = 1

        for raw in raw_slides:
            slide = self._as_dict(raw)
            if not slide:
                warnings.append("Bỏ qua slide payload không hợp lệ")
                continue
            if slide.get("slide_type") == "exercise":
                exercise_slides, slide_answers = self._exercise_models(slide, question_number)
                question_number += len(slide_answers)
                answers.extend(slide_answers)
                planned.extend(exercise_slides)
                continue
            planned.extend(self._content_models(slide, warnings))

        for index, chunk in enumerate(self._chunks(answers, 4), start=1):
            title = "Đáp án và giải thích"
            if len(answers) > 4:
                title += f" ({index}/{(len(answers) + 3) // 4})"
            planned.append(RenderSlideModel(
                slide_id=f"answer_key_{index}",
                logical_slide_id="answer_key",
                slide_type="answer_key",
                layout_id="EDU_ANSWER_KEY",
                title=title,
                answer_entries=list(chunk),
            ))

        return RenderPlan(
            slides=planned,
            source_slide_count=len(raw_slides),
            warnings=warnings,
        )

    def _content_models(self, slide: dict, warnings: List[str]) -> List[RenderSlideModel]:
        slide_type = slide.get("slide_type") or "content"
        title = str(slide.get("title") or "Nội dung")
        blocks = [self._as_dict(block) for block in slide.get("blocks") or []]
        blocks = [block for block in blocks if block]
        if not blocks:
            bullets = slide.get("bullets") or slide.get("key_points") or []
            if bullets:
                blocks = [{"type": "bullets", "items": [str(item) for item in bullets]}]

        expanded: List[dict] = []
        for block in blocks or [{"type": "bullets", "items": []}]:
            expanded.extend(self._expand_block(block, warnings))

        if slide_type == "title":
            return self._title_models(slide, title, expanded)
        if slide_type == "summary":
            return [
                self._model(
                    slide,
                    "EDU_SUMMARY",
                    title if index == 1 else f"{title} (tiếp theo)",
                    [block],
                    suffix=index,
                )
                for index, block in enumerate(expanded or [{}], start=1)
            ]

        models = []
        media = self._select_media(slide)
        for index, block in enumerate(expanded or [{}], start=1):
            block_type = block.get("type", "bullets")
            physical_title = title if index == 1 else f"{title} (tiếp theo)"
            if block_type in RICH_LAYOUTS:
                layout_id = RICH_LAYOUTS[block_type]
                block_media = None
            elif media:
                layout_id = "EDU_CONTENT_MEDIA"
                block_media = media if index == 1 else None
            else:
                layout_id = "EDU_CONTENT"
                block_media = None
            models.append(self._model(
                slide,
                layout_id,
                physical_title,
                [block] if block else [],
                media=block_media,
                suffix=index,
            ))
        return models

    def _title_models(self, slide: dict, title: str, blocks: List[dict]) -> List[RenderSlideModel]:
        text_lines: List[str] = []
        rich_blocks: List[dict] = []
        for block in blocks:
            kind = block.get("type")
            if kind == "bullets":
                text_lines.extend(str(item) for item in block.get("items") or [])
            elif kind in {"paragraph", "callout"}:
                text_lines.append(str(block.get("text") or ""))
            else:
                rich_blocks.append(block)

        models = [self._model(
            slide,
            "EDU_TITLE",
            title,
            [{"type": "bullets", "items": text_lines[:3]}] if text_lines else [],
        )]
        continuation_blocks = [
            {"type": "bullets", "items": list(chunk)}
            for chunk in self._chunks(text_lines[3:], 5)
        ]
        continuation_blocks.extend(rich_blocks)
        for index, block in enumerate(continuation_blocks, start=2):
            layout_id = RICH_LAYOUTS.get(block.get("type"), "EDU_CONTENT")
            models.append(self._model(
                slide,
                layout_id,
                f"{title} (tiếp theo)",
                [block],
                suffix=index,
            ))
        return models

    def _exercise_models(self, slide: dict, start_number: int):
        questions = [self._as_dict(q) for q in slide.get("questions") or []]
        questions = [q for q in questions if q]
        if not questions:
            return [self._model(
                slide,
                "EDU_EXERCISE",
                str(slide.get("title") or "Bài tập luyện tập"),
                [{"type": "bullets", "items": slide.get("bullets") or []}],
            )], []

        answers = []
        models = []
        total = (len(questions) + 1) // 2
        for chunk_index, chunk in enumerate(self._chunks(questions, 2), start=1):
            numbered = []
            notes = []
            for question in chunk:
                number = start_number + len(answers)
                item = dict(question)
                item["number"] = number
                numbered.append(item)
                answer = {
                    "number": number,
                    "answer": question.get("correct_answer") or question.get("answer") or "",
                    "explanation": question.get("explanation") or "",
                }
                answers.append(answer)
                notes.append(
                    f"Câu {number}: {answer['answer']}"
                    + (f" — {answer['explanation']}" if answer["explanation"] else "")
                )
            title = str(slide.get("title") or "Bài tập luyện tập")
            if total > 1:
                title += f" ({chunk_index}/{total})"
            model = self._model(slide, "EDU_EXERCISE", title, [], suffix=chunk_index)
            model.questions = numbered
            model.notes = "\n".join(filter(None, [model.notes, *notes]))
            models.append(model)
        return models, answers

    def _expand_block(self, block: dict, warnings: List[str]) -> List[dict]:
        block_type = block.get("type")
        if block_type == "bullets":
            return self._split_bullets(block)
        if block_type == "paragraph":
            sentences = self._sentences(str(block.get("text") or ""))
            return [{**block, "text": text} for text in self._pack_text(sentences, 650)] or [block]
        if block_type == "code":
            lines = str(block.get("code") or "").splitlines()
            return [{**block, "code": "\n".join(chunk)} for chunk in self._split_code(lines)] or [block]
        if block_type == "table":
            columns = list(block.get("columns") or [])
            rows = list(block.get("rows") or [])
            if not columns or any(len(row) != len(columns) for row in rows):
                warnings.append("Table không hợp lệ được chuyển thành bullets")
                return [{
                    "type": "bullets",
                    "items": [" | ".join(map(str, row)) for row in ([columns] + rows) if row],
                    "source_chunk_ids": block.get("source_chunk_ids") or [],
                }]
            return self._split_table(block)
        if block_type == "chart":
            categories = list(block.get("categories") or [])
            series = list(block.get("series") or [])
            if not categories or not series or any(
                len(item.get("values") or []) != len(categories) for item in series
            ):
                warnings.append("Chart không hợp lệ được chuyển thành bullets")
                return [{
                    "type": "bullets",
                    "items": [str(item) for item in categories] or [str(block.get("caption") or "Dữ liệu biểu đồ")],
                    "source_chunk_ids": block.get("source_chunk_ids") or [],
                }]
            return self._split_chart(block, warnings)
        if block_type == "process":
            if len(block.get("steps") or []) < 2:
                warnings.append("Process thiếu bước được chuyển thành bullets")
                return [{
                    "type": "bullets",
                    "items": block.get("steps") or [],
                    "source_chunk_ids": block.get("source_chunk_ids") or [],
                }]
            return [{**block, "steps": list(chunk)} for chunk in self._chunks(block.get("steps") or [], 6)] or [block]
        if block_type == "comparison":
            left = list(block.get("left_items") or [])
            right = list(block.get("right_items") or [])
            if not left or not right:
                warnings.append("Comparison thiếu một phía được chuyển thành bullets")
                return [{
                    "type": "bullets",
                    "items": [*left, *right],
                    "source_chunk_ids": block.get("source_chunk_ids") or [],
                }]
            count = max((len(left) + 4) // 5, (len(right) + 4) // 5, 1)
            return [
                {**block, "left_items": left[i * 5:(i + 1) * 5], "right_items": right[i * 5:(i + 1) * 5]}
                for i in range(count)
            ]
        return [block]

    def _split_bullets(self, block: dict) -> List[dict]:
        items: List[str] = []
        for raw_item in block.get("items") or []:
            item = str(raw_item)
            if len(item) <= 650:
                items.append(item)
                continue
            sentences = self._sentences(item)
            items.extend(self._pack_text(sentences, 650) or [item])

        groups: List[List[str]] = []
        current: List[str] = []
        weighted_characters = 0
        for item in items:
            item_weight = max(len(item), 1)
            if current and (len(current) >= 5 or weighted_characters + item_weight > 650):
                groups.append(current)
                current = []
                weighted_characters = 0
            current.append(item)
            weighted_characters += item_weight
        if current:
            groups.append(current)
        return [{**block, "items": group} for group in groups] or [block]

    @staticmethod
    def _split_code(lines: List[str]) -> List[List[str]]:
        chunks: List[List[str]] = []
        remaining = list(lines)
        while remaining:
            if len(remaining) <= 18:
                chunks.append(remaining)
                break
            window = remaining[:18]
            candidates = [
                index for index, line in enumerate(window[8:], start=8)
                if not line.strip() or line.lstrip().startswith(("def ", "class "))
            ]
            split_at = (candidates[-1] + 1) if candidates else 18
            chunks.append(remaining[:split_at])
            remaining = remaining[split_at:]
        return chunks

    def _split_table(self, block: dict) -> List[dict]:
        columns = list(block.get("columns") or [])
        rows = list(block.get("rows") or [])
        index_groups = [list(range(len(columns)))] if len(columns) <= 6 else [
            [0, *range(index, min(index + 5, len(columns)))]
            for index in range(1, len(columns), 5)
        ]
        results = []
        for indices in index_groups:
            group = [columns[index] for index in indices]
            projected = [[row[index] for index in indices] for row in rows]
            for chunk in self._chunks(projected, 8):
                results.append({**block, "columns": group, "rows": list(chunk)})
        return results or [block]

    def _split_chart(self, block: dict, warnings: List[str]) -> List[dict]:
        categories = list(block.get("categories") or [])
        series = list(block.get("series") or [])
        if block.get("chart_type") in {"pie", "doughnut"} and len(series) > 1:
            warnings.append("Pie/doughnut nhiều series được chuyển sang column chart")
            block = {**block, "chart_type": "column"}
        results = []
        for series_chunk in self._chunks(series, 4):
            for start in range(0, len(categories), 8):
                stop = start + 8
                results.append({
                    **block,
                    "categories": categories[start:stop],
                    "series": [
                        {**item, "values": list(item.get("values") or [])[start:stop]}
                        for item in series_chunk
                    ],
                })
        return results or [block]

    def _model(self, slide, layout_id, title, blocks, *, media=None, suffix=1):
        slide_id = str(slide.get("slide_id") or "slide")
        sources = [str(item) for item in slide.get("source_chunk_ids") or []]
        for block in blocks:
            for source in block.get("source_chunk_ids") or []:
                source = str(source)
                if source not in sources:
                    sources.append(source)
        return RenderSlideModel(
            slide_id=slide_id if suffix == 1 else f"{slide_id}_{suffix}",
            logical_slide_id=slide_id,
            slide_type=str(slide.get("slide_type") or "content"),
            layout_id=layout_id,
            title=title,
            blocks=blocks,
            media=media,
            notes=str(slide.get("notes") or ""),
            source_chunk_ids=sources,
        )

    @staticmethod
    def _select_media(slide: dict):
        media = [SlideRenderPlanner._as_dict(item) for item in slide.get("media") or []]
        media = [item for item in media if item]
        return max(media, key=lambda item: item.get("relevance_score") or -1) if media else None

    @staticmethod
    def _sentences(text: str) -> List[str]:
        return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]

    @staticmethod
    def _pack_text(parts: Iterable[str], limit: int) -> List[str]:
        packed, current = [], ""
        for part in parts:
            candidate = f"{current} {part}".strip()
            if current and len(candidate) > limit:
                packed.append(current)
                current = part
            else:
                current = candidate
        if current:
            packed.append(current)
        return packed

    @staticmethod
    def _chunks(items: List[Any], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]

    @staticmethod
    def _as_dict(value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            return value
        if hasattr(value, "model_dump"):
            return value.model_dump()
        return {}


__all__ = ["SlideRenderPlanner"]
