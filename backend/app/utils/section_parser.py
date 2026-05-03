import re

SECTION_PATTERNS = {
    "summary": r"(summary|profile|about me)",
    "skills": r"(skills|technical skills|technologies)",
    "projects": r"(projects|project experience)",
    "experience": r"(experience|work experience|employment)",
    "education": r"(education|academic background)"
}


def parse_sections(text: str):
    if not text:
        return {"sections": {}, "confidence": {}}

    text_lower = text.lower()

    matches = []

    for section, pattern in SECTION_PATTERNS.items():
        for match in re.finditer(pattern, text_lower):
            matches.append((match.start(), match.end(), section))

    matches.sort(key=lambda x: x[0])

    sections = {key: "" for key in SECTION_PATTERNS}
    confidence = {key: 0.0 for key in SECTION_PATTERNS}

    for i, (start, end, section) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)

        content = text[end:next_start].strip()

        if content:
            sections[section] = content
            confidence[section] = min(1.0, len(content.split()) / 120)

    return {
        "sections": sections,
        "confidence": confidence
    }