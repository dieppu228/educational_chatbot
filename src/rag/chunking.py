import re
import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import Counter


# ============================================================
# 1. CẤU TRÚC DỮ LIỆU (DATA CLASSES)
# ============================================================

@dataclass
class ChunkMetadata:
    """
    Metadata cho mỗi chunk.
    
    Giải thích từng trường:
        - book: Bộ sách (VD: "CD" = Cánh Diều, "KNTT" = Kết nối tri thức)
        - grade: Lớp học (VD: "10", "11", "12")
        - topic: Mã chủ đề (VD: "A", "B", "1", "2")
        - topic_name: Tên đầy đủ chủ đề 
        - lesson: Số bài (VD: "Bài 1", "Bài 2")
        - lesson_name: Tên đầy đủ bài học
        - section: Mã mục (VD: "1", "2", "a")
        - title: Tiêu đề heading
        - level: Cấp heading markdown (1 = #, 2 = ##, 3 = ###)
        - type: Loại nội dung (theory/exercise/summary/objective/note/application)
    """
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


@dataclass
class Chunk:
    """
    Một chunk trong hệ thống hierarchical chunking.
    
    Giải thích:
        - content: Nội dung text thuần
        - context: Breadcrumb path (VD: "CHỦ ĐỀ A > Bài 1 > 2. Mục chính")
        - metadata: Thông tin phân loại
    """
    content: str = ""
    context: str = ""
    metadata: ChunkMetadata = field(default_factory=ChunkMetadata)


# ============================================================
# 2. PARSER: ĐỌC FILE MARKDOWN VÀ TÁCH SECTIONS
# ============================================================

def parse_heading(line: str) -> Optional[Tuple[int, str]]:
    """
    Phân tích 1 dòng heading Markdown.
    
    Args:
        line: Dòng text
        
    Returns:
        Tuple(level, title) nếu là heading, None nếu không.
        
    Ví dụ:
        "# Bài 1: DỮ LIỆU" → (1, "Bài 1: DỮ LIỆU")
        "## 1. Nguồn thông tin" → (2, "1. Nguồn thông tin")
        "Dòng thường" → None
    """
    match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
    if match:
        level = len(match.group(1))
        title = match.group(2).strip()
        return (level, title)
    return None


def detect_topic_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Phát hiện dòng CHỦ ĐỀ (có thể là heading # hoặc bold **).
    
    Patterns cần detect:
        - "# CHỦ ĐỀ A: Máy tính và xã hội tri thức..."
        - "# CHỦ ĐỀ 1: Máy tính và xã hội tri thức"
        - "# CHỦ ĐỀ A (CS): ..."
        - "**CHỦ ĐỀ A : ...**"
        
    Returns:
        Tuple(topic_code, topic_name) hoặc None.
        
    Ví dụ:
        "# CHỦ ĐỀ A: Máy tính và xã hội tri thức" 
            → ("A", "Máy tính và xã hội tri thức")
        "# CHỦ ĐỀ 2: Mạng máy tính và Internet"
            → ("2", "Mạng máy tính và Internet")
    """
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
    """
    Phát hiện heading bài học từ title (đã bỏ # markers).
    
    Patterns:
        - "Bài 1: DỮ LIỆU, THÔNG TIN VÀ XỬ LÍ THÔNG TIN"
        - "Bài 1: DỮ LIỆU VÀ THÔNG TIN – Phần 2"
        
    Returns:
        Tuple(lesson_num, lesson_name) hoặc None.
        
    Ví dụ:
        "Bài 1: DỮ LIỆU VÀ THÔNG TIN" → ("Bài 1", "DỮ LIỆU VÀ THÔNG TIN")
    """
    pattern = r'^(Bài\s+\d+)\s*[:\-–]\s*(.+)$'
    match = re.match(pattern, title, re.IGNORECASE)
    if match:
        lesson_num = match.group(1).strip()
        lesson_name = match.group(2).strip()
        return (lesson_num, lesson_name)
    
    return None


def classify_section_type(title: str) -> str:
    """
    Phân loại loại nội dung dựa trên tiêu đề section.
    
    Quy tắc phân loại:
        - "Luyện tập", "LUYỆN TẬP", "Bài tập" → exercise
        - "Vận dụng", "VẬN DỤNG" → application
        - "Tóm tắt bài học", "TÓM TẮT" → summary
        - "Em cần chú ý", "Chú ý" → note
        - "Sau bài này em sẽ", "Học xong bài này" → objective
        - "Hoạt động", "Kết nối tri thức" → theory (mặc định)
        - Mọi thứ khác → theory
        
    Args:
        title: Tiêu đề section
        
    Returns:
        str: Loại nội dung
    """
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


# ============================================================
# 3. HIERARCHICAL CHUNKER (CORE)
# ============================================================

class HierarchicalChunker:
    """
    Chunker phân cấp cho sách giáo khoa Markdown.
    
    Thuật toán:
    1. Đọc file markdown theo từng dòng
    2. Khi gặp heading, tạo chunk mới với metadata tương ứng
    3. Nội dung giữa 2 heading liên tiếp → content của chunk
    4. Duy trì stack chủ đề / bài hiện tại để tạo breadcrumb context
    5. Phân loại type dựa trên tiêu đề section
    
    Quy tắc đặc biệt:
    - CHỦ ĐỀ: Không tạo chunk, chỉ cập nhật state
    - Bài: Không tạo chunk riêng cho heading bài, gom phần mở đầu vào chunk đầu tiên  
    - Chunk quá ngắn (<min_chars): Gộp vào chunk trước đó
    - Chunk quá dài (>max_chars): Cắt theo paragraph
    """
    
    def __init__(self, min_chunk_chars: int = 100, max_chunk_chars: int = 2000):
        """
        Khởi tạo chunker.
        
        Args:
            min_chunk_chars: Chunk nhỏ hơn sẽ bị gộp vào chunk trước
            max_chunk_chars: Chunk lớn hơn sẽ bị cắt theo paragraph
        """
        self.min_chunk_chars = min_chunk_chars
        self.max_chunk_chars = max_chunk_chars
    
    def _extract_book_grade(self, filename: str) -> Tuple[str, str]:
        """
        Trích xuất thông tin bộ sách và lớp từ tên file.
        
        Quy ước tên file: SGK_Tin{grade}_{book}_clean.md
        
        Ví dụ:
            "SGK_Tin10_CD_clean.md" → ("CD", "10")
            "SGK_Tin11_KNTT_clean.md" → ("KNTT", "11")
        """
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
    
    def _build_context(self, topic_name: str, lesson_name: str, 
                       section_title: str) -> str:
        """
        Tạo breadcrumb context string từ các thành phần hierarchical.
        
        Ví dụ:
            ("Máy tính và xã hội tri thức", "DỮ LIỆU VÀ THÔNG TIN", "Nguồn thông tin")
            → "Máy tính và xã hội tri thức > DỮ LIỆU VÀ THÔNG TIN > Nguồn thông tin"
        """
        parts = []
        if topic_name:
            parts.append(topic_name)
        if lesson_name:
            parts.append(lesson_name)
        if section_title:
            parts.append(section_title)
        return " > ".join(parts)
    
    def _detect_objective_block(self, lines: List[str], start_idx: int) -> Optional[int]:
        """
        Phát hiện phần mục tiêu bài học (dạng inline, không có heading).
        
        Patterns:
            - "Học xong bài này, em sẽ:"
            - "SAU BÀI NÀY EM SẼ:" (có thể là heading ##)
            
        Returns:
            Index dòng cuối của block mục tiêu, hoặc None.
        """
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
        """
        Chunk 1 file markdown thành danh sách Chunk.
        
        Đây là hàm chính của pipeline. Thuật toán:
        
        1. Đọc toàn bộ file, chia theo dòng
        2. Scan qua từng dòng:
           a. Gặp CHỦ ĐỀ → cập nhật current_topic
           b. Gặp Bài → cập nhật current_lesson  
           c. Gặp heading ## hoặc ### → flush chunk hiện tại, bắt đầu chunk mới
           d. Dòng thường → gom vào content chunk hiện tại
        3. Post-process: gộp chunk nhỏ, cắt chunk to
        
        Args:
            filepath: Đường dẫn file .md
            
        Returns:
            List[Chunk]: Danh sách chunks
        """
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
            """Lưu chunk hiện tại vào danh sách."""
            nonlocal current_content_lines, current_title, current_level, current_type
            
            text = '\n'.join(current_content_lines).strip()
            if not text:
                return
            
            context = self._build_context(
                current_topic_name, current_lesson_name, current_title
            )
            
            chunk = Chunk(
                content=text,
                context=context,
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
        
        return chunks
    
    def _merge_short_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """
        Gộp các chunk quá ngắn vào chunk trước đó.
        
        Lý do: Chunk quá ngắn (< min_chunk_chars) không đủ context cho retrieval,
        gây nhiễu khi search. Gộp vào chunk trước giúp mỗi chunk có đủ nội dung.
        
        Quy tắc: Chỉ gộp nếu cùng bài (lesson) và chunk trước cùng type.
        """
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
        """
        Cắt chunk quá dài thành nhiều chunk nhỏ hơn, theo paragraph.
        
        Lý do: Chunk quá dài (> max_chunk_chars) giảm precision khi retrieval
        vì embedding bị "pha loãng". Cắt theo paragraph giữ ngữ nghĩa tốt hơn
        so với cắt theo ký tự.
        """
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
                        context=chunk.context,
                        metadata=ChunkMetadata(**asdict(chunk.metadata))
                    )
                    if part_num > 1:
                        new_chunk.metadata.title += f" (phần {part_num})"
                    result.append(new_chunk)
                    current_text = para
                    part_num += 1
                else:
                    current_text += ('\n\n' + para if current_text else para)
            
            if current_text.strip():
                new_chunk = Chunk(
                    content=current_text.strip(),
                    context=chunk.context,
                    metadata=ChunkMetadata(**asdict(chunk.metadata))
                )
                if part_num > 1:
                    new_chunk.metadata.title += f" (phần {part_num})"
                result.append(new_chunk)
        
        return result
    
    def chunk_all_files(self, data_dir: str, pattern: str = "*_clean.md") -> List[Chunk]:
        """
        Chạy chunking trên tất cả file matching pattern trong thư mục.
        
        Args:
            data_dir: Thư mục chứa file markdown
            pattern: Glob pattern để filter file
            
        Returns:
            List[Chunk]: Toàn bộ chunks từ tất cả file
        """
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


# ============================================================
# 4. EXPORT: XUẤT CHUNKS RA JSON
# ============================================================

def chunks_to_json(chunks: List[Chunk]) -> List[Dict]:
    """
    Chuyển danh sách Chunk thành list dict (JSON-serializable).
    
    Format output:
    {
        "content": "...",
        "context": "CHỦ ĐỀ A > Bài 1 > Mục 2",
        "metadata": { ... }
    }
    """
    result = []
    for chunk in chunks:
        result.append({
            "content": chunk.content,
            "context": chunk.context,
            "metadata": asdict(chunk.metadata)
        })
    return result


def save_chunks(chunks: List[Chunk], output_path: str):
    """Lưu chunks vào file JSON. Tạo thư mục nếu chưa có."""
    data = chunks_to_json(chunks)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} chunks to {output_path}")


# ============================================================
# 5. THỐNG KÊ & KIỂM TRA
# ============================================================

def print_stats(chunks: List[Chunk]):
    """In thống kê chi tiết về kết quả chunking."""
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
    """
    Kiểm tra nhanh n chunks ngẫu nhiên.
    
    Hiển thị: context, type, độ dài, 100 ký tự đầu.
    """
    import random
    
    print("\n" + "=" * 60)
    print(f"SPOT CHECK ({n} random chunks)")
    print("=" * 60)
    
    samples = random.sample(chunks, min(n, len(chunks)))
    
    for i, chunk in enumerate(samples, 1):
        meta = chunk.metadata
        print(f"\n--- Chunk {i} ---")
        print(f"  Context: {chunk.context}")
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
    PROJECT_DIR = SCRIPT_DIR.parent
    
    RAW_DATA_DIR = str(PROJECT_DIR / "RawData")
    OUTPUT_PATH = str(PROJECT_DIR / "data" / "rag_chunks_v2.json")
    
    # === Chạy chunking ===
    chunker = HierarchicalChunker(
        min_chunk_chars=100,   # Gộp chunk < 100 chars
        max_chunk_chars=2000,  # Cắt chunk > 2000 chars
    )
    
    all_chunks = chunker.chunk_all_files(RAW_DATA_DIR, pattern="*_clean.md")
    
    # === Thống kê ===
    print_stats(all_chunks)
    
    # === Spot check ===
    spot_check(all_chunks, n=5)
    
    # === Lưu file ===
    save_chunks(all_chunks, OUTPUT_PATH)
    
    print("\nPipeline completed successfully!")
