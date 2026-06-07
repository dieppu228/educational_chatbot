import re
import json
import os
import hashlib
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import Counter

from src.config.config import settings


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU (DATA CLASSES)
# ============================================================

@dataclass
class ChunkMetadata:
    book: str = ""
    grade: str = ""
    topic: str = ""
    topic_name: str = ""
    lesson: str = ""
    lesson_name: str = ""
    section: str = ""
    title: str = ""
    level: int = 0
    type: str = "theory"
    source_path: str = ""
    chunk_index: int = 0


@dataclass
class Chunk:
    chunk_id: str = ""
    content: str = ""
    breadcrumb: str = ""
    metadata: ChunkMetadata = field(default_factory=ChunkMetadata)

    @property
    def context(self) -> str:
        return self.breadcrumb

    @context.setter
    def context(self, value: str) -> None:
        self.breadcrumb = value


# ============================================================
# 2. PARSER: ĐỌC FILE MARKDOWN VÀ TÁCH SECTIONS
# ============================================================

def parse_heading(line: str) -> Optional[Tuple[int, str]]:
    match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
    if match:
        level = len(match.group(1))
        title = match.group(2).strip()
        return (level, title)
    return None


def detect_topic_line(line: str) -> Optional[Tuple[str, str]]:
    # Loại bỏ heading markers và bold markers
    text = re.sub(r'^#+\s*', '', line.strip())
    text = re.sub(r'^\*\*|\*\*$', '', text).strip()
    
    # Pattern: CHỦ ĐỀ <code>: <name> hoặc CHỦ ĐỀ <code> (<variant>): <name>
    pattern = r'CHỦ\s+ĐỀ\s+([A-Za-z0-9]+(?:\s*\([^)]*\))?)\s*[:\-–]\s*(.+)'
    match = re.match(pattern, text, re.IGNORECASE)
    if match:
        topic_code = match.group(1).strip()
        topic_name = match.group(2).strip()
        # Loại bỏ trailing bold markers nếu còn
        topic_name = re.sub(r'\*\*$', '', topic_name).strip()
        return (topic_code, topic_name)
    
    return None


def detect_lesson_line(title: str) -> Optional[Tuple[str, str]]:
    pattern = r'^(Bài\s+\d+)\s*[:\-–]\s*(.+)$'
    match = re.match(pattern, title, re.IGNORECASE)
    if match:
        lesson_num = match.group(1).strip()
        lesson_name = match.group(2).strip()
        return (lesson_num, lesson_name)
    
    return None


def classify_section_type(title: str) -> str:
    title_lower = title.lower().strip()
    
    # Exercise patterns
    if re.search(r'luyện\s*tập|bài\s*tập', title_lower):
        return "exercise"
    
    # Application patterns
    if re.search(r'vận\s*dụng', title_lower):
        return "application"
    
    # Summary patterns  
    if re.search(r'tóm\s*tắt', title_lower):
        return "summary"
    
    # Note patterns
    if re.search(r'em\s+cần\s+chú\s+ý|chú\s+ý', title_lower):
        return "note"
    
    # Objective patterns
    if re.search(r'sau\s+bài\s+.*em\s+sẽ|học\s+xong\s+bài', title_lower):
        return "objective"
    
    # Default
    return "theory"


VALID_CHUNK_TYPES = ("theory", "exercise", "application", "summary", "note", "objective")


def content_fingerprint(content: str) -> str:
    normalized = re.sub(r'\s+', ' ', content).strip()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def build_chunk_id(
    book: str,
    grade: str,
    topic: str,
    lesson: str,
    breadcrumb: str,
    chunk_index: int,
    content: str,
) -> str:
    raw = "|".join([
        book,
        grade,
        topic,
        lesson,
        breadcrumb,
        str(chunk_index),
        content_fingerprint(content),
    ])
    return str(uuid.uuid5(uuid.NAMESPACE_URL, raw))


def lesson_sort_key(path: Path) -> Tuple[int, str]:
    match = re.match(r'bai([A-Za-z0-9]+)', path.stem, re.IGNORECASE)
    if not match:
        return (10_000, path.stem)
    lesson_no = match.group(1)
    if lesson_no.isdigit():
        return (int(lesson_no), path.stem)
    return (10_000, lesson_no)


class ChunkTypeClassifier:
    def __init__(
        self,
        cache_path: str,
        model_name: str = "gemini-2.5-flash-lite",
        batch_size: int = 20,
        timeout_seconds: int = 45,
        enabled: bool = True,
    ):
        self.cache_path = Path(cache_path)
        self.model_name = model_name
        self.batch_size = batch_size
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled
        self.cache = self._load_cache()
        self.client = None

    def _load_cache(self) -> dict:
        if not self.cache_path.exists():
            return {}
        try:
            with self.cache_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with self.cache_path.open("w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _cache_key(self, chunk: Chunk) -> str:
        meta = chunk.metadata
        raw = "|".join([
            meta.book,
            meta.grade,
            meta.topic,
            meta.lesson,
            chunk.breadcrumb,
            meta.title,
            content_fingerprint(chunk.content),
        ])
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def _get_client(self):
        if self.client is not None:
            return self.client
        api_key = settings.GENAI_API_KEY or os.getenv("GENAI_API_KEY", "")
        if not api_key:
            raise RuntimeError("GENAI_API_KEY is not set")
        from google import genai
        from google.genai import types
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=self.timeout_seconds * 1000),
        )
        return self.client

    def _prompt(self, items: list[dict]) -> str:
        return (
            "Bạn phân loại các chunk nội dung SGK Tin học THPT.\n"
            "Chỉ chọn đúng một type trong danh sách: "
            "theory, exercise, application, summary, note, objective.\n\n"
            "Quy ước:\n"
            "- objective: mục tiêu bài học, thường có 'Học xong bài này' hoặc 'Sau bài này em sẽ'.\n"
            "- exercise: luyện tập, bài tập, câu hỏi kiểm tra trong bài.\n"
            "- application: vận dụng, nhiệm vụ áp dụng kiến thức vào tình huống thực tế.\n"
            "- summary: tóm tắt bài học hoặc tổng kết kiến thức.\n"
            "- note: ghi chú/lưu ý/cảnh báo/nhấn mạnh cần nhớ.\n"
            "- theory: phần còn lại, gồm khái niệm, giải thích, ví dụ, hướng dẫn thực hành.\n\n"
            "Trả về JSON object duy nhất dạng {\"items\":[{\"id\":0,\"type\":\"theory\"}]}.\n"
            "Không giải thích.\n\n"
            f"Chunks:\n{json.dumps(items, ensure_ascii=False)}"
        )

    def _parse_response(self, text: str) -> dict[int, str]:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        data = json.loads(cleaned)
        result = {}
        for item in data.get("items", []):
            idx = int(item.get("id"))
            chunk_type = str(item.get("type", "")).strip().lower()
            if chunk_type in VALID_CHUNK_TYPES:
                result[idx] = chunk_type
        return result

    def classify(self, chunks: list[Chunk]) -> list[Chunk]:
        if not self.enabled:
            return chunks

        pending: list[tuple[int, str, Chunk]] = []
        for idx, chunk in enumerate(chunks):
            key = self._cache_key(chunk)
            cached = self.cache.get(key)
            if cached in VALID_CHUNK_TYPES:
                chunk.metadata.type = cached
            else:
                pending.append((idx, key, chunk))

        if not pending:
            print("LLM chunk type classification: all chunks loaded from cache")
            return chunks

        print(f"LLM chunk type classification: {len(pending)} uncached chunks")
        try:
            client = self._get_client()
        except Exception as exc:
            print(f"LLM classifier unavailable, keeping heuristic types: {exc}")
            return chunks

        for start in range(0, len(pending), self.batch_size):
            batch = pending[start : start + self.batch_size]
            prompt_items = []
            for local_id, (_, _, chunk) in enumerate(batch):
                prompt_items.append({
                    "id": local_id,
                    "breadcrumb": chunk.breadcrumb,
                    "section_title": chunk.metadata.title,
                    "current_heuristic_type": chunk.metadata.type,
                    "content_preview": chunk.content[:900],
                })

            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=self._prompt(prompt_items),
                )
                parsed = self._parse_response(getattr(response, "text", "") or "")
            except Exception as exc:
                print(f"  batch {start // self.batch_size + 1}: LLM failed, keeping heuristic types: {exc}")
                continue

            for local_id, chunk_type in parsed.items():
                if not (0 <= local_id < len(batch)):
                    continue
                _, key, chunk = batch[local_id]
                chunk.metadata.type = chunk_type
                self.cache[key] = chunk_type

            self._save_cache()
            print(f"  classified {min(start + len(batch), len(pending))}/{len(pending)}")

        return chunks


# ============================================================
# 3. HIERARCHICAL CHUNKER (CORE)
# ============================================================

class HierarchicalChunker:
    
    def __init__(self, min_chunk_chars: int = 100, max_chunk_chars: int = 2000):
        self.min_chunk_chars = min_chunk_chars
        self.max_chunk_chars = max_chunk_chars
    
    def _extract_book_grade(self, filename: str) -> Tuple[str, str]:
        # Tìm grade
        grade_match = re.search(r'Tin(\d{2})', filename)
        grade = grade_match.group(1) if grade_match else ""
        
        # Tìm book
        if 'KNTT' in filename.upper():
            book = "KNTT"
        elif 'CD' in filename.upper():
            book = "CD"
        else:
            book = "UNKNOWN"
        
        return (book, grade)

    def _extract_lesson_from_filename(self, filepath: Path) -> str:
        match = re.match(r'bai([A-Za-z0-9]+)', filepath.stem, re.IGNORECASE)
        if not match:
            return ""
        lesson_no = match.group(1).upper()
        return f"Bài {lesson_no}"

    def _read_topic_metadata(self, topic_dir: Path) -> Tuple[str, str]:
        readme_path = topic_dir / "README.md"
        if readme_path.exists():
            for line in readme_path.read_text(encoding="utf-8").splitlines():
                topic_info = detect_topic_line(line)
                if topic_info:
                    return topic_info

        match = re.search(r'chu_de_([^_]+)_(.+)$', topic_dir.name)
        if not match:
            return "", topic_dir.name

        topic_code = match.group(1).upper()
        topic_name = match.group(2).replace("_", " ")
        return topic_code, topic_name
    
    def _build_context(self, topic_name: str, lesson_name: str, 
                       section_title: str) -> str:
        parts = []
        if topic_name:
            parts.append(topic_name)
        if lesson_name:
            parts.append(lesson_name)
        if section_title:
            parts.append(section_title)
        return " > ".join(parts)

    def _assign_chunk_ids(self, chunks: List[Chunk]) -> List[Chunk]:
        lesson_counters: Dict[Tuple[str, str, str, str], int] = {}
        for chunk in chunks:
            meta = chunk.metadata
            key = (meta.book, meta.grade, meta.topic, meta.lesson)
            lesson_counters[key] = lesson_counters.get(key, 0) + 1
            meta.chunk_index = lesson_counters[key]
            chunk.chunk_id = build_chunk_id(
                book=meta.book,
                grade=meta.grade,
                topic=meta.topic,
                lesson=meta.lesson,
                breadcrumb=chunk.breadcrumb,
                chunk_index=meta.chunk_index,
                content=chunk.content,
            )
        return chunks
    
    def _detect_objective_block(self, lines: List[str], start_idx: int) -> Optional[int]:
        line = lines[start_idx].strip()
        line_lower = line.lower()
        
        # Kiểm tra pattern
        if not re.search(r'học\s+xong\s+bài|sau\s+bài\s+.*em\s+sẽ', line_lower):
            return None
        
        # Tìm hết block (các dòng * tiếp theo)
        end_idx = start_idx + 1
        while end_idx < len(lines):
            next_line = lines[end_idx].strip()
            if next_line.startswith('*') or next_line == '':
                end_idx += 1
            else:
                break
        
        return end_idx
    
    def chunk_file(self, filepath: str) -> List[Chunk]:
        filename = Path(filepath).name
        book, grade = self._extract_book_grade(filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # === State variables ===
        current_topic = ""       # Mã chủ đề (A, B, 1, 2...)
        current_topic_name = ""  # Tên chủ đề
        current_lesson = ""      # Bài X
        current_lesson_name = "" # Tên bài
        
        chunks: List[Chunk] = []
        current_content_lines: List[str] = []
        current_title = ""
        current_level = 0
        current_type = "theory"
        
        def flush_chunk():
            nonlocal current_content_lines, current_title, current_level, current_type
            
            text = '\n'.join(current_content_lines).strip()
            if not text:
                return
            
            context = self._build_context(
                current_topic_name, current_lesson_name, current_title
            )
            
            chunk = Chunk(
                content=text,
                breadcrumb=context,
                metadata=ChunkMetadata(
                    book=book,
                    grade=grade,
                    topic=current_topic,
                    topic_name=current_topic_name,
                    lesson=current_lesson,
                    lesson_name=current_lesson_name,
                    section="",
                    title=current_title,
                    level=current_level,
                    type=current_type,
                    source_path=filepath,
                )
            )
            chunks.append(chunk)
            current_content_lines = []
        
        # === Main loop: scan qua từng dòng ===
        i = 0
        while i < len(lines):
            line = lines[i]
            line_stripped = line.strip()
            
            # --- Bỏ qua dòng trống ở đầu ---
            if not line_stripped and not current_content_lines:
                i += 1
                continue
            
            # --- Check: Dòng CHỦ ĐỀ (bold hoặc heading) ---
            topic_info = detect_topic_line(line_stripped)
            if topic_info:
                flush_chunk()
                current_topic, current_topic_name = topic_info
                # Reset lesson khi sang chủ đề mới
                current_lesson = ""
                current_lesson_name = ""
                current_title = ""
                current_type = "theory"
                i += 1
                continue
            
            # --- Check: Heading ---
            heading = parse_heading(line_stripped)
            if heading:
                level, title = heading
                
                # Check nếu heading chứa CHỦ ĐỀ
                topic_info = detect_topic_line(title)
                if topic_info:
                    flush_chunk()
                    current_topic, current_topic_name = topic_info
                    current_lesson = ""
                    current_lesson_name = ""
                    current_title = ""
                    current_type = "theory"
                    i += 1
                    continue
                
                # Check: Heading bài học (# Bài X: ...)
                lesson_info = detect_lesson_line(title)
                if lesson_info and level == 1:
                    flush_chunk()
                    current_lesson, current_lesson_name = lesson_info
                    current_title = ""
                    current_type = "theory"
                    current_level = 1
                    i += 1
                    continue
                
                # --- Heading mục chính / mục con ---
                flush_chunk()
                current_title = title
                current_level = level
                current_type = classify_section_type(title)
                i += 1
                continue
            
            # --- Check: Mục tiêu bài học (inline, không heading) ---
            obj_end = self._detect_objective_block(lines, i)
            if obj_end is not None:
                flush_chunk()
                current_title = "Mục tiêu bài học"
                current_level = 2
                current_type = "objective"
                # Gom toàn bộ block mục tiêu
                current_content_lines = [l.rstrip() for l in lines[i:obj_end]]
                flush_chunk()
                current_title = ""
                current_type = "theory"
                i = obj_end
                continue
            
            # --- Dòng nội dung thường ---
            current_content_lines.append(line.rstrip())
            i += 1
        
        # Flush chunk cuối cùng
        flush_chunk()
        
        # === Post-process ===
        chunks = self._merge_short_chunks(chunks)
        chunks = self._split_long_chunks(chunks)
        chunks = self._assign_chunk_ids(chunks)
        
        return chunks

    def chunk_lesson_file(
        self,
        filepath: str,
        book: str,
        grade: str,
        topic: str,
        topic_name: str,
    ) -> List[Chunk]:
        path = Path(filepath)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        current_topic = topic
        current_topic_name = topic_name
        current_lesson = self._extract_lesson_from_filename(path)
        current_lesson_name = ""

        chunks: List[Chunk] = []
        current_content_lines: List[str] = []
        current_title = ""
        current_level = 0
        current_type = "theory"

        def flush_chunk():
            nonlocal current_content_lines, current_title, current_level, current_type

            text = '\n'.join(current_content_lines).strip()
            if not text:
                return

            context = self._build_context(
                current_topic_name, current_lesson_name, current_title
            )

            chunk = Chunk(
                content=text,
                breadcrumb=context,
                metadata=ChunkMetadata(
                    book=book,
                    grade=grade,
                    topic=current_topic,
                    topic_name=current_topic_name,
                    lesson=current_lesson,
                    lesson_name=current_lesson_name,
                    section="",
                    title=current_title,
                    level=current_level,
                    type=current_type,
                    source_path=str(path.relative_to(Path(__file__).resolve().parents[2])),
                )
            )
            chunks.append(chunk)
            current_content_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            line_stripped = line.strip()

            if not line_stripped and not current_content_lines:
                i += 1
                continue

            heading = parse_heading(line_stripped)
            if heading:
                level, title = heading

                lesson_info = detect_lesson_line(title)
                if lesson_info and level <= 2 and not current_lesson_name:
                    current_lesson, current_lesson_name = lesson_info
                    current_title = ""
                    current_type = "theory"
                    current_level = level
                    i += 1
                    continue

                topic_info = detect_topic_line(title)
                if topic_info:
                    i += 1
                    continue

                flush_chunk()
                if not current_lesson_name and level <= 2:
                    current_lesson_name = title
                    current_title = ""
                    current_type = "theory"
                    current_level = level
                else:
                    current_title = title
                    current_level = level
                    current_type = classify_section_type(title)
                i += 1
                continue

            obj_end = self._detect_objective_block(lines, i)
            if obj_end is not None:
                flush_chunk()
                current_title = "Mục tiêu bài học"
                current_level = 2
                current_type = "objective"
                current_content_lines = [l.rstrip() for l in lines[i:obj_end]]
                flush_chunk()
                current_title = ""
                current_type = "theory"
                i = obj_end
                continue

            current_content_lines.append(line.rstrip())
            i += 1

        flush_chunk()

        chunks = self._merge_short_chunks(chunks)
        chunks = self._split_long_chunks(chunks)
        chunks = self._assign_chunk_ids(chunks)

        return chunks
    
    def _merge_short_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        if not chunks:
            return chunks
        
        merged = [chunks[0]]
        
        for chunk in chunks[1:]:
            content_len = len(chunk.content.strip())
            prev = merged[-1]
            
            # Gộp nếu quá ngắn VÀ cùng bài VÀ cùng type
            if (content_len < self.min_chunk_chars 
                and chunk.metadata.lesson == prev.metadata.lesson
                and chunk.metadata.type == prev.metadata.type):
                prev.content += '\n\n' + chunk.content
            else:
                merged.append(chunk)
        
        return merged
    
    def _split_long_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        result = []
        
        for chunk in chunks:
            if len(chunk.content) <= self.max_chunk_chars:
                result.append(chunk)
                continue
            
            # Cắt theo paragraph (2 dòng trống)
            paragraphs = re.split(r'\n\s*\n', chunk.content)
            current_text = ""
            part_num = 1
            
            for para in paragraphs:
                if len(current_text) + len(para) + 2 > self.max_chunk_chars and current_text:
                    # Tạo chunk mới
                    new_chunk = Chunk(
                        content=current_text.strip(),
                        breadcrumb=chunk.breadcrumb,
                        metadata=ChunkMetadata(**asdict(chunk.metadata))
                    )
                    result.append(new_chunk)
                    current_text = para
                    part_num += 1
                else:
                    current_text += ('\n\n' + para if current_text else para)
            
            if current_text.strip():
                new_chunk = Chunk(
                    content=current_text.strip(),
                    breadcrumb=chunk.breadcrumb,
                    metadata=ChunkMetadata(**asdict(chunk.metadata))
                )
                result.append(new_chunk)
        
        return result
    
    def chunk_all_files(self, data_dir: str, pattern: str = "*_clean.md") -> List[Chunk]:
        data_path = Path(data_dir)
        files = sorted(data_path.glob(pattern))
        
        all_chunks = []
        
        print(f"Directory: {data_dir}")
        print(f"Found {len(files)} files matching '{pattern}'")
        print("=" * 60)
        
        for filepath in files:
            # Bỏ qua file TEST
            if 'TEST' in filepath.name:
                print(f"  Skipping: {filepath.name}")
                continue
            
            chunks = self.chunk_file(str(filepath))
            all_chunks.extend(chunks)
            
            # Thống kê
            type_counts = Counter(c.metadata.type for c in chunks)
            print(f"  {filepath.name}: {len(chunks)} chunks")
            for t, cnt in sorted(type_counts.items()):
                print(f"      {t}: {cnt}")
        
        print("=" * 60)
        print(f"TOTAL: {len(all_chunks)} chunks from {len(files)} files")
        
        return all_chunks

    def chunk_structured_books(self, project_dir: str) -> List[Chunk]:
        project_path = Path(project_dir)
        all_chunks = []
        files = []

        for book in ("CD", "KNTT"):
            book_dir = project_path / book
            if not book_dir.exists():
                continue

            for grade_dir in sorted(p for p in book_dir.iterdir() if p.is_dir()):
                if not re.fullmatch(r'\d{2}', grade_dir.name):
                    continue

                for topic_dir in sorted(p for p in grade_dir.iterdir() if p.is_dir()):
                    topic, topic_name = self._read_topic_metadata(topic_dir)
                    for lesson_file in sorted(topic_dir.glob("bai*.md"), key=lesson_sort_key):
                        files.append((book, grade_dir.name, topic, topic_name, lesson_file))

        print(f"Structured books root: {project_dir}")
        print(f"Found {len(files)} lesson files")
        print("=" * 60)

        for book, grade, topic, topic_name, lesson_file in files:
            chunks = self.chunk_lesson_file(
                str(lesson_file),
                book=book,
                grade=grade,
                topic=topic,
                topic_name=topic_name,
            )
            all_chunks.extend(chunks)
            type_counts = Counter(c.metadata.type for c in chunks)
            print(f"  {lesson_file.relative_to(project_path)}: {len(chunks)} chunks")
            for t, cnt in sorted(type_counts.items()):
                print(f"      {t}: {cnt}")

        print("=" * 60)
        print(f"TOTAL: {len(all_chunks)} chunks from {len(files)} lesson files")

        return all_chunks


# ============================================================
# 4. EXPORT: XUẤT CHUNKS RA JSON
# ============================================================

def chunks_to_json(chunks: List[Chunk]) -> List[Dict]:
    result = []
    for chunk in chunks:
        meta = chunk.metadata
        full_content = f"{chunk.breadcrumb} : {chunk.content}" if chunk.breadcrumb else chunk.content
        result.append({
            "chunk_id": chunk.chunk_id,
            "content": chunk.content,
            "full_content": full_content,
            "breadcrumb": chunk.breadcrumb,
            "book": meta.book,
            "grade": meta.grade,
            "topic": meta.topic,
            "topic_name": meta.topic_name,
            "lesson": meta.lesson,
            "lesson_name": meta.lesson_name,
            "section_title": meta.title,
            "level": meta.level,
            "type": meta.type,
            "source_path": meta.source_path,
            "chunk_index": meta.chunk_index,
        })
    return result


def save_chunks(chunks: List[Chunk], output_path: str):
    data = chunks_to_json(chunks)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} chunks to {output_path}")


# ============================================================
# 5. THỐNG KÊ & KIỂM TRA
# ============================================================

def print_stats(chunks: List[Chunk]):
    print("\n" + "=" * 60)
    print("CHUNK STATISTICS")
    print("=" * 60)
    
    # Tổng quan
    print(f"\n{'Total chunks:':<30} {len(chunks)}")
    
    content_lengths = [len(c.content) for c in chunks]
    if content_lengths:
        print(f"{'Average length:':<30} {sum(content_lengths)/len(content_lengths):.0f} chars")
        print(f"{'Shortest chunk:':<30} {min(content_lengths)} chars")
        print(f"{'Longest chunk:':<30} {max(content_lengths)} chars")
    
    # Phân bố theo type
    print(f"\n--- By content type ---")
    type_counts = Counter(c.metadata.type for c in chunks)
    for t, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:<20} {cnt:>5} ({cnt/len(chunks)*100:.1f}%)")
    
    # Phân bố theo sách
    print(f"\n--- By book ---")
    book_counts = Counter(c.metadata.book for c in chunks)
    for b, cnt in sorted(book_counts.items()):
        print(f"  {b:<20} {cnt:>5}")
    
    # Phân bố theo lớp
    print(f"\n--- By grade ---")
    grade_counts = Counter(c.metadata.grade for c in chunks)
    for g, cnt in sorted(grade_counts.items()):
        print(f"  Grade {g:<16} {cnt:>5}")
    
    # Phân bố theo chủ đề
    print(f"\n--- By topic (top 10) ---")
    topic_counts = Counter(
        f"{c.metadata.book} {c.metadata.grade} - {c.metadata.topic}: {c.metadata.topic_name[:30]}" 
        for c in chunks if c.metadata.topic
    )
    for t, cnt in topic_counts.most_common(10):
        print(f"  {t:<50} {cnt:>3}")


def spot_check(chunks: List[Chunk], n: int = 5):
    import random
    
    print("\n" + "=" * 60)
    print(f"SPOT CHECK ({n} random chunks)")
    print("=" * 60)
    
    samples = random.sample(chunks, min(n, len(chunks)))
    
    for i, chunk in enumerate(samples, 1):
        meta = chunk.metadata
        print(f"\n--- Chunk {i} ---")
        print(f"  Breadcrumb: {chunk.breadcrumb}")
        print(f"  {meta.book} grade {meta.grade} | Topic: {meta.topic} | {meta.lesson}")
        print(f"  Type: {meta.type} | Title: {meta.title}")
        print(f"  Length: {len(chunk.content)} chars")
        preview = chunk.content[:150].replace('\n', ' ')
        print(f"  Preview: {preview}...")


# ============================================================
# 6. MAIN: CHẠY PIPELINE
# ============================================================

if __name__ == "__main__":
    # === Cấu hình (dùng absolute path dựa trên vị trí script) ===
    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_DIR = SCRIPT_DIR.parents[1]
    
    RAW_DATA_DIR = str(PROJECT_DIR / "RawData")
    OUTPUT_PATH = str(PROJECT_DIR / "data" / "rag_chunks_v2.json")
    
    # === Chạy chunking ===
    chunker = HierarchicalChunker(
        min_chunk_chars=100,   # Gộp chunk < 100 chars
        max_chunk_chars=2000,  # Cắt chunk > 2000 chars
    )
    
    if (PROJECT_DIR / "CD").exists() or (PROJECT_DIR / "KNTT").exists():
        all_chunks = chunker.chunk_structured_books(str(PROJECT_DIR))
    else:
        all_chunks = chunker.chunk_all_files(RAW_DATA_DIR, pattern="*_clean.md")
    
    # === Thống kê ===
    print_stats(all_chunks)
    
    # === Spot check ===
    spot_check(all_chunks, n=5)
    
    # === Lưu file ===
    save_chunks(all_chunks, OUTPUT_PATH)
    
    print("\nPipeline completed successfully!")
