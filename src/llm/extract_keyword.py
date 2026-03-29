import json
from google import genai
from google.genai.types import GenerateContentConfig
import os, re
from src.prompts.extract_prompts import EXTRACT_PROMPT


GRADE_REGEX = re.compile(
    r"(?:lớp|lop|khối|khoi|grade)\s*(10|11|12)",
    re.IGNORECASE
)

def extract_grade_lesson(query: str, api_key: str):
    # --- 1. Regex extract grade ---
    grade = None
    match = GRADE_REGEX.search(query)
    if match:
        grade = match.group(1)

    # --- 2. LLM extract lesson ---
    client = genai.Client(api_key=api_key)
    prompt = EXTRACT_PROMPT.format(query=query)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt,
        config=GenerateContentConfig(temperature=0.0)
    )

    raw = ""
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                raw += part.text

    # --- Clean markdown ---
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"^```", "", raw)
    raw = re.sub(r"```$", "", raw)
    raw = raw.strip()

    # --- Parse JSON ---
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return grade, None

    lesson = data.get("lesson")

    # --- Validate lesson ---
    if lesson is not None and not isinstance(lesson, str):
        lesson = None

    if isinstance(lesson, str):
        lesson = lesson.strip()
        if lesson == "":
            lesson = None

    return grade, lesson