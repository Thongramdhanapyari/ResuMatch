import re

SECTION_PATTERNS = {
    "summary": r"(summary|profile|about me)",
    "skills": r"(skills|technical skills|technologies)",
    "projects": r"(projects|project experience)",
    "experience": r"(experience|work experience|employment)",
    "education": r"(education|academic background)"
}


def parse_sections(text: str):
    text_lower = text.lower()

    sections = {}
    confidence = {}

    for section, pattern in SECTION_PATTERNS.items():
        matches = list(re.finditer(pattern, text_lower))

        if matches:
            # Take first match as anchor point
            start = matches[0].end()

            # Find next section or end of text
            next_positions = [
                m.start() for m in re.finditer(r"\n[a-z ]{3,30}\n", text_lower[start:])
            ]

            end = start + next_positions[0] if next_positions else len(text_lower)

            section_text = text[start:end].strip()

            sections[section] = section_text
            confidence[section] = min(1.0, len(section_text.split()) / 100)

        else:
            sections[section] = ""
            confidence[section] = 0.0

    return {
        "sections": sections,
        "confidence": confidence
    }