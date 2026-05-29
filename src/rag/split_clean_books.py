import re
import shutil
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_DIR / "RawData"


@dataclass
class Lesson:
    number: str
    title: str
    lines: list[str] = field(default_factory=list)


@dataclass
class Topic:
    code: str
    title: str
    lines: list[str] = field(default_factory=list)
    lessons: list[Lesson] = field(default_factory=list)


def strip_markdown_heading(line: str) -> str:
    text = re.sub(r"^#{1,6}\s*", "", line.strip())
    return text.strip()


def slugify(value: str, max_len: int = 90) -> str:
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.replace("đ", "d").replace("Đ", "D")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:max_len].strip("_") or "untitled"


def parse_source_name(path: Path) -> tuple[str, str]:
    match = re.match(r"SGK_Tin(?P<grade>\d{2})_(?P<book>CD|KNTT)_clean\.md$", path.name)
    if not match:
        raise ValueError(f"Unsupported source file name: {path.name}")
    return match.group("book"), match.group("grade")


def detect_topic(line: str) -> Optional[tuple[str, str]]:
    text = strip_markdown_heading(line)
    match = re.match(
        r"CHỦ\s*ĐỀ\s+([A-Z0-9]+(?:\s*\([^)]*\))?)\s*[:\-–]\s*(.+)$",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    code = re.sub(r"\s+", " ", match.group(1).strip())
    title = re.sub(r"\s+", " ", match.group(2).strip())
    return code, title


def detect_lesson(line: str) -> Optional[tuple[str, str]]:
    heading_match = re.match(r"^(#{1,2})\s+(.+)$", line.strip())
    if not heading_match:
        return None

    text = heading_match.group(2).strip()
    if re.match(r"BÀI\s+(TÌM|ĐỌC)", text, re.IGNORECASE):
        return None

    match = re.match(r"Bài\s+([0-9]+|[A-Z])\s*:\s*(.+)$", text, re.IGNORECASE)
    if not match:
        return None

    number = match.group(1).strip().upper()
    title = re.sub(r"\s+", " ", match.group(2).strip())
    return number, title


def detect_fallback_lesson(line: str) -> Optional[str]:
    heading_match = re.match(r"^(#{1,2})\s+(.+)$", line.strip())
    if not heading_match:
        return None

    title = heading_match.group(2).strip()
    if detect_topic(line):
        return None
    if re.match(r"BÀI\s+(TÌM|ĐỌC)", title, re.IGNORECASE):
        return None
    return re.sub(r"\s+", " ", title)


def lesson_number_as_int(value: str) -> Optional[int]:
    return int(value) if value.isdigit() else None


def should_start_lesson(book: str, current_topic: Topic, lesson_no: str) -> bool:
    if not current_topic.lessons:
        return True

    new_no = lesson_number_as_int(lesson_no)
    last_no = lesson_number_as_int(current_topic.lessons[-1].number)

    if new_no is None or last_no is None:
        return lesson_no != current_topic.lessons[-1].number

    if new_no <= last_no:
        return False

    if book == "CD":
        return new_no == last_no + 1

    return True


def parse_book(path: Path) -> tuple[str, str, list[Topic], list[str]]:
    book, grade = parse_source_name(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    topics: list[Topic] = []
    preface: list[str] = []
    current_topic: Optional[Topic] = None
    current_lesson: Optional[Lesson] = None

    for line in lines:
        topic_info = detect_topic(line)
        if topic_info:
            code, title = topic_info
            current_topic = Topic(code=code, title=title, lines=[line])
            topics.append(current_topic)
            current_lesson = None
            continue

        if current_topic is None:
            if line.strip():
                preface.append(line)
            continue

        lesson_info = detect_lesson(line)
        if lesson_info and should_start_lesson(book, current_topic, lesson_info[0]):
            lesson_no, lesson_title = lesson_info
            current_lesson = Lesson(number=lesson_no, title=lesson_title, lines=[line])
            current_topic.lessons.append(current_lesson)
            continue

        fallback_title = detect_fallback_lesson(line)
        if fallback_title and not current_topic.lessons and current_lesson is None:
            current_lesson = Lesson(number="1", title=fallback_title, lines=[line])
            current_topic.lessons.append(current_lesson)
            continue

        if current_lesson is not None:
            current_lesson.lines.append(line)
        else:
            current_topic.lines.append(line)

    return book, grade, topics, preface


def topic_dir_name(topic: Topic, index: int) -> str:
    code = slugify(topic.code, max_len=20)
    title = slugify(topic.title, max_len=70)
    return f"{index:02d}_chu_de_{code}_{title}"


def lesson_file_name(lesson: Lesson) -> str:
    return f"bai{slugify(lesson.number, max_len=20)}.md"


def write_markdown(path: Path, lines: Iterable[str]) -> None:
    text = "\n".join(lines).strip() + "\n"
    path.write_text(text, encoding="utf-8")


def reset_grade_dir(book: str, grade: str) -> Path:
    grade_dir = PROJECT_DIR / book / grade
    if grade_dir.exists():
        shutil.rmtree(grade_dir)
    grade_dir.mkdir(parents=True, exist_ok=True)
    return grade_dir


def split_file(path: Path) -> dict[str, object]:
    book, grade, topics, preface = parse_book(path)
    grade_dir = reset_grade_dir(book, grade)

    if preface:
        write_markdown(grade_dir / "README.md", preface)

    total_lessons = 0
    warnings: list[str] = []

    for index, topic in enumerate(topics, start=1):
        topic_dir = grade_dir / topic_dir_name(topic, index)
        topic_dir.mkdir(parents=True, exist_ok=True)
        write_markdown(topic_dir / "README.md", topic.lines)

        if not topic.lessons:
            warnings.append(f"{book} {grade} {topic.code}: no lessons detected")

        seen_files: set[str] = set()
        for lesson in topic.lessons:
            filename = lesson_file_name(lesson)
            if filename in seen_files:
                suffix = slugify(lesson.title, max_len=40)
                filename = f"{filename.removesuffix('.md')}_{suffix}.md"
            seen_files.add(filename)
            write_markdown(topic_dir / filename, lesson.lines)
            total_lessons += 1

    return {
        "book": book,
        "grade": grade,
        "topics": len(topics),
        "lessons": total_lessons,
        "warnings": warnings,
    }


def main() -> None:
    sources = sorted(RAW_DATA_DIR.glob("SGK_Tin*_clean.md"))
    if not sources:
        raise SystemExit(f"No *_clean.md files found in {RAW_DATA_DIR}")

    print(f"Found {len(sources)} clean source files")
    all_warnings: list[str] = []
    for source in sources:
        result = split_file(source)
        print(
            f"{source.name}: {result['book']}/{result['grade']} "
            f"topics={result['topics']} lessons={result['lessons']}"
        )
        all_warnings.extend(result["warnings"])

    if all_warnings:
        print("\nWarnings:")
        for warning in all_warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
