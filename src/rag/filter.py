def filter_by_grade(chunks, grade=None, fallback_all=True):
    if grade is None:
        return chunks if fallback_all else []

    grade = str(grade).strip()

    filtered = []
    for c in chunks:
        meta = c.get("metadata", {}) or c.get("meta", {})

        g = meta.get("grade") or meta.get("Grade")
        if g is None:
            continue

        if str(g).strip() == grade:
            filtered.append(c)

    if not filtered and fallback_all:
        print("WARNING: No chunk matched grade, fallback to all")
        return chunks

    return filtered
