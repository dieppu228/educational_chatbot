"""
OCR Pipeline: PDF → Markdown (sử dụng Gemini Vision API)

Pipeline gồm 2 bước:
    1. OCR: PDF → Markdown thô (Gemini vision đọc ảnh từng trang)
    2. Clean: Markdown thô → Markdown phân cấp heading chuẩn

Cải thiện so với scan_text.ipynb:
    - Retry logic khi API lỗi
    - Rate limiting tránh bị block
    - Resume từ trang cuối nếu bị gián đoạn
    - Smart chunking theo heading thay vì dấu câu
    - API key từ .env
    - System prompt tối ưu cho SGK
    
Usage:
    python scan_text.py                          # Chạy mặc định
    python scan_text.py --step ocr               # Chỉ chạy bước OCR
    python scan_text.py --step clean              # Chỉ chạy bước clean
    python scan_text.py --pdf "path/to/file.pdf"  # Chỉ định file PDF
"""

import os
import re
import sys
import time
import argparse
from pathlib import Path
from typing import List, Optional

# === Thêm project root vào path ===
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import fitz  # PyMuPDF
from PIL import Image
import google.generativeai as genai


# ============================================================
# SYSTEM PROMPTS
# ============================================================

OCR_SYSTEM_PROMPT = """\
Bạn là chuyên gia trích xuất văn bản từ sách giáo khoa Tin học THPT Việt Nam.

=== NHIỆM VỤ ===
Trích xuất **CHỈ nội dung văn bản** từ ảnh trang sách, xuất ra dạng Markdown sạch.

=== QUY TẮC BẮT BUỘC ===

1. **GIỮ NGUYÊN NỘI DUNG GỐC:**
   - Giữ nguyên 100% nội dung văn bản, không tóm tắt, không diễn giải lại
   - Giữ nguyên thuật ngữ chuyên ngành, tên riêng, ví dụ cụ thể
   - Giữ nguyên câu hỏi, bài tập, phần "Tóm tắt bài học", phần "Em cần chú ý"

2. **BỎ QUA HOÀN TOÀN (KHÔNG đề cập):**
   - Hình ảnh, ảnh minh họa, ảnh chụp màn hình
   - Bảng biểu, biểu đồ, sơ đồ
   - Icon, logo, hình trang trí
   - Số trang, header/footer trang
   - Watermark, dòng chữ "Đọc sách tại hoc10.vn" hoặc tương tự
   - Chú thích hình ảnh (caption dạng "Hình 1.1", "Ảnh minh họa...")

3. **XỬ LÝ CODE/MÃ NGUỒN:**
   - KHÔNG giữ code gốc
   - Thay bằng mô tả ngắn: "Đoạn mã này có chức năng [mô tả]"
   - Giữ lại kết quả output nếu có

4. **ĐỊNH DẠNG MARKDOWN:**
   - Tiêu đề bài lớn: `# Bài X: TÊN BÀI`
   - Mục chính: `## Tên mục`
   - Mục con: `### Tên mục con`
   - Nội dung: dùng `*` cho gạch đầu dòng
   - In đậm cho khái niệm quan trọng: `**khái niệm**`
   - In nghiêng cho thuật ngữ mới: `*thuật ngữ*`

5. **KHÔNG THÊM:**
   - Không thêm lời giới thiệu, không thêm nhận xét
   - Không thêm "Trang X" vào output
   - Chỉ xuất Markdown thuần túy
"""


CLEAN_SYSTEM_PROMPT = """\
Bạn là chuyên gia phân cấp tài liệu Markdown.

=== NHIỆM VỤ ===
Phân cấp lại cấu trúc heading cho đoạn Markdown được cung cấp.

=== QUY TẮC ===
1. Giữ nguyên 100% nội dung văn bản, KHÔNG tóm tắt hay xóa bất kỳ dòng nào
2. Chỉ sửa lại cấp heading cho đúng:
   - `#` cho Chủ đề/Bài lớn (VD: # Bài 1: DỮ LIỆU VÀ THÔNG TIN)
   - `##` cho Mục chính (VD: ## 1) Nguồn thông tin và dữ liệu)
   - `###` cho Mục con (VD: ### a) Từ thông tin thành dữ liệu)
   - `####` trở đi cho tiểu mục nhỏ hơn
3. Xóa các dòng rác: "--- Trang X ---", watermark, header/footer lặp lại
4. Giữ nguyên các phần: bài tập, câu hỏi, tóm tắt bài học
5. Trả về Markdown sạch, không thêm giải thích
"""


# ============================================================
# CẤU HÌNH
# ============================================================

class Config:
    """Cấu hình cho pipeline OCR."""
    
    # API
    API_KEY: str = os.getenv("GENAI_API_KEY", "")
    OCR_MODEL: str = "gemini-2.5-flash"
    CLEAN_MODEL: str = "gemini-2.0-flash"
    
    # OCR settings
    DPI: int = 200
    TEMP_DIR: str = "temp_images"
    
    # Rate limiting
    DELAY_BETWEEN_PAGES: float = 2.0       # Giây giữa mỗi trang OCR
    DELAY_BETWEEN_CHUNKS: float = 1.5      # Giây giữa mỗi chunk clean
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 10.0              # Giây chờ khi retry
    
    # Chunking
    MAX_CHUNK_CHARS: int = 9000


# ============================================================
# BƯỚC 1: OCR - PDF → Markdown thô
# ============================================================

def ocr_pdf_to_markdown(
    pdf_path: str,
    output_path: str,
    start_page: int,
    end_page: int,
    config: Config = Config()
) -> str:
    """
    OCR từng trang PDF bằng Gemini Vision → ghi ra file Markdown.
    
    Hỗ trợ resume: nếu file output đã có nội dung, sẽ detect trang cuối
    đã OCR và tiếp tục từ trang tiếp theo.
    
    Args:
        pdf_path: Đường dẫn file PDF
        output_path: Đường dẫn file output .md
        start_page: Trang bắt đầu (0-indexed)
        end_page: Trang kết thúc (exclusive)
        config: Cấu hình
    
    Returns:
        str: Đường dẫn file output
    """
    if not config.API_KEY:
        raise ValueError("GENAI_API_KEY chưa được set trong .env")
    
    genai.configure(api_key=config.API_KEY)
    
    # Khởi tạo model (1 lần duy nhất)
    model = genai.GenerativeModel(
        model_name=config.OCR_MODEL,
        system_instruction=OCR_SYSTEM_PROMPT
    )
    
    # Mở PDF
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    end_page = min(end_page, total_pages)
    
    print(f"📄 PDF: {pdf_path}")
    print(f"📑 Tổng số trang PDF: {total_pages}")
    print(f"🎯 OCR từ trang {start_page + 1} đến trang {end_page}")
    
    # Tạo thư mục temp
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    
    # === Resume detection ===
    resume_page = start_page
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing = f.read()
        
        # Tìm trang cuối đã OCR
        page_markers = re.findall(r"<!-- PAGE (\d+) -->", existing)
        if page_markers:
            last_done = max(int(p) for p in page_markers)
            resume_page = last_done  # Đã OCR xong trang last_done (0-indexed), bắt đầu từ trang tiếp
            print(f"⏩ Resume: đã OCR xong đến trang {last_done}, tiếp tục từ trang {resume_page + 1}")
    
    if resume_page >= end_page:
        print("✅ Tất cả các trang đã được OCR!")
        return output_path
    
    # === OCR từng trang ===
    success_count = 0
    fail_count = 0
    
    with open(output_path, "a", encoding="utf-8") as f_out:
        for page_idx in range(resume_page, end_page):
            page_num = page_idx + 1  # Hiển thị 1-indexed
            
            # Render trang thành ảnh
            page = doc.load_page(page_idx)
            pix = page.get_pixmap(dpi=config.DPI)
            img_path = os.path.join(config.TEMP_DIR, f"page_{page_num}.png")
            pix.save(img_path)
            
            # Gọi Gemini OCR với retry
            page_text = _ocr_single_page(model, img_path, page_num, config)
            
            if page_text:
                # Ghi marker để hỗ trợ resume + nội dung
                f_out.write(f"<!-- PAGE {page_idx} -->\n")
                f_out.write(page_text.strip() + "\n\n")
                f_out.flush()
                success_count += 1
                print(f"  ✅ Trang {page_num}/{end_page} — {len(page_text)} ký tự")
            else:
                fail_count += 1
                f_out.write(f"<!-- PAGE {page_idx} -->\n")
                f_out.write(f"<!-- OCR FAILED: trang {page_num} -->\n\n")
                f_out.flush()
                print(f"  ❌ Trang {page_num}/{end_page} — OCR thất bại")
            
            # Xóa ảnh temp
            try:
                os.remove(img_path)
            except OSError:
                pass
            
            # Rate limiting
            if page_idx < end_page - 1:
                time.sleep(config.DELAY_BETWEEN_PAGES)
    
    doc.close()
    
    print(f"\n{'=' * 50}")
    print(f"🎉 OCR hoàn tất!")
    print(f"   ✅ Thành công: {success_count} trang")
    print(f"   ❌ Thất bại: {fail_count} trang")
    print(f"   📝 Output: {output_path}")
    
    return output_path


def _ocr_single_page(model, img_path: str, page_num: int, config: Config) -> Optional[str]:
    """OCR 1 trang với retry logic."""
    
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            image = Image.open(img_path)
            
            response = model.generate_content([
                f"Trích xuất toàn bộ văn bản tiếng Việt từ ảnh trang sách giáo khoa Tin học này.",
                image
            ])
            
            # Parse response
            page_text = ""
            if hasattr(response, "parts") and response.parts:
                for part in response.parts:
                    if hasattr(part, "text"):
                        page_text += part.text
            
            if page_text.strip():
                return page_text.strip()
            else:
                print(f"  ⚠️  Trang {page_num}: response rỗng (attempt {attempt}/{config.MAX_RETRIES})")
                
        except Exception as e:
            print(f"  ⚠️  Trang {page_num}: lỗi '{str(e)[:60]}' (attempt {attempt}/{config.MAX_RETRIES})")
            
            if attempt < config.MAX_RETRIES:
                print(f"       Retry sau {config.RETRY_DELAY}s...")
                time.sleep(config.RETRY_DELAY)
    
    return None


# ============================================================
# BƯỚC 2: CLEAN - Markdown thô → Markdown phân cấp
# ============================================================

def clean_markdown(
    input_path: str,
    output_path: str,
    config: Config = Config()
) -> str:
    """
    Phân cấp lại heading và làm sạch Markdown.
    
    Chunking thông minh: split theo heading `#` thay vì dấu câu,
    giữ nguyên cấu trúc section.
    
    Args:
        input_path: File Markdown thô (output từ bước OCR)
        output_path: File Markdown sạch
        config: Cấu hình
    
    Returns:
        str: Đường dẫn file output
    """
    if not config.API_KEY:
        raise ValueError("GENAI_API_KEY chưa được set trong .env")
    
    genai.configure(api_key=config.API_KEY)
    
    # Khởi tạo model 1 lần
    model = genai.GenerativeModel(
        model_name=config.CLEAN_MODEL,
        system_instruction=CLEAN_SYSTEM_PROMPT
    )
    
    # Đọc file input
    with open(input_path, "r", encoding="utf-8") as f:
        raw_md = f.read()
    
    # Xóa page markers
    raw_md = re.sub(r"<!-- PAGE \d+ -->\n?", "", raw_md)
    raw_md = re.sub(r"<!-- OCR FAILED: trang \d+ -->\n?", "", raw_md)
    
    # Smart chunking theo heading
    chunks = _smart_chunk(raw_md, max_chars=config.MAX_CHUNK_CHARS)
    print(f"📦 Input: {input_path} ({len(raw_md)} chars)")
    print(f"🔹 Chia thành {len(chunks)} chunks")
    
    # Process từng chunk
    results = []
    for i, chunk in enumerate(chunks):
        print(f"  ⚙️  Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)...", end=" ")
        
        cleaned = _clean_single_chunk(model, chunk, config)
        if cleaned:
            results.append(cleaned)
            print(f"✅ → {len(cleaned)} chars")
        else:
            results.append(chunk)  # Giữ nguyên nếu clean thất bại
            print("⚠️ giữ nguyên")
        
        if i < len(chunks) - 1:
            time.sleep(config.DELAY_BETWEEN_CHUNKS)
    
    # Ghi output
    final_text = "\n\n".join(results)
    
    # Post-processing: xóa các dòng rác phổ biến
    final_text = _post_process(final_text)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    
    print(f"\n🎉 Clean hoàn tất! → {output_path} ({len(final_text)} chars)")
    return output_path


def _smart_chunk(text: str, max_chars: int = 9000) -> List[str]:
    """
    Chia text theo heading (#) thay vì dấu câu.
    Đảm bảo mỗi chunk bắt đầu bằng heading (nếu có)
    và không vượt quá max_chars.
    """
    # Split theo heading level 1 hoặc 2
    sections = re.split(r"(?=^#{1,2}\s)", text, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]
    
    chunks = []
    current_chunk = ""
    
    for section in sections:
        # Nếu thêm section vào mà vẫn trong giới hạn → gộp
        if len(current_chunk) + len(section) + 2 <= max_chars:
            current_chunk += "\n\n" + section if current_chunk else section
        else:
            # Lưu chunk hiện tại
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Nếu section đơn lẻ > max_chars → cắt nhỏ hơn
            if len(section) > max_chars:
                sub_chunks = _fallback_chunk(section, max_chars)
                chunks.extend(sub_chunks)
                current_chunk = ""
            else:
                current_chunk = section
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [text]


def _fallback_chunk(text: str, max_chars: int) -> List[str]:
    """Chunk dự phòng: split theo paragraph khi section quá dài."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current += "\n\n" + para if current else para
        else:
            if current:
                chunks.append(current.strip())
            current = para
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks


def _clean_single_chunk(model, chunk: str, config: Config) -> Optional[str]:
    """Clean 1 chunk với retry."""
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            response = model.generate_content([
                "Phân cấp lại heading cho đoạn Markdown sau, giữ nguyên nội dung:",
                chunk
            ])
            
            result = ""
            if hasattr(response, "parts") and response.parts:
                for part in response.parts:
                    if hasattr(part, "text"):
                        result += part.text
            
            if result.strip():
                return result.strip()
                
        except Exception as e:
            print(f"\n    ⚠️ Lỗi: {str(e)[:50]} (attempt {attempt})")
            if attempt < config.MAX_RETRIES:
                time.sleep(config.RETRY_DELAY)
    
    return None


def _post_process(text: str) -> str:
    """Xóa các dòng rác phổ biến trong SGK đã OCR."""
    # Xóa watermark / quảng cáo
    patterns_to_remove = [
        r"Đọc sách tại hoc10\.vn\s*",
        r"Nguồn:?\s*hoc10\.vn\s*",
        r"```\s*```",                          # Code block rỗng
        r"\n{4,}",                             # Nhiều hơn 3 dòng trống liên tiếp
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "\n", text, flags=re.IGNORECASE)
    
    # Chuẩn hóa xuống dòng: tối đa 2 dòng trống
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="OCR Pipeline: PDF → Markdown")
    parser.add_argument("--step", choices=["ocr", "clean", "both"], default="both",
                        help="Chạy bước nào (default: both)")
    parser.add_argument("--pdf", type=str, default=None,
                        help="Đường dẫn file PDF")
    parser.add_argument("--start", type=int, default=6,
                        help="Trang bắt đầu, 0-indexed (default: 6)")
    parser.add_argument("--end", type=int, default=163,
                        help="Trang kết thúc, exclusive (default: 163)")
    parser.add_argument("--raw-output", type=str, default=None,
                        help="File output Markdown thô (default: auto từ tên PDF)")
    parser.add_argument("--clean-output", type=str, default=None,
                        help="File output Markdown sạch (default: auto)")
    
    args = parser.parse_args()
    config = Config()
    
    # Auto-generate output paths từ tên PDF
    if args.pdf:
        base_name = Path(args.pdf).stem.replace(" ", "_")
    else:
        base_name = "SGK_output"
    
    raw_output = args.raw_output or f"RawData/{base_name}.md"
    clean_output = args.clean_output or f"RawData/{base_name}_clean.md"
    
    print("=" * 60)
    print("📖 OCR PIPELINE: PDF → Markdown")
    print("=" * 60)
    
    if args.step in ("ocr", "both"):
        if not args.pdf:
            print("❌ Cần chỉ định --pdf khi chạy bước OCR")
            sys.exit(1)
        
        print(f"\n{'─' * 40}")
        print("BƯỚC 1: OCR")
        print(f"{'─' * 40}")
        ocr_pdf_to_markdown(
            pdf_path=args.pdf,
            output_path=raw_output,
            start_page=args.start,
            end_page=args.end,
            config=config
        )
    
    if args.step in ("clean", "both"):
        print(f"\n{'─' * 40}")
        print("BƯỚC 2: CLEAN")
        print(f"{'─' * 40}")
        
        raw_file = raw_output
        if not os.path.exists(raw_file):
            print(f"❌ Không tìm thấy file: {raw_file}")
            sys.exit(1)
        
        clean_markdown(
            input_path=raw_file,
            output_path=clean_output,
            config=config
        )
    
    print(f"\n{'=' * 60}")
    print("✅ PIPELINE HOÀN TẤT!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
