import re
from app.utils.skills_catalog import SKILL_CATALOG
from app.utils.skill_normalizer import normalize_skill


def extract_skills(text: str) -> set:
    if not text:
        return set()

    text_lower = text.lower()
    found_skills = set()

    for skills in SKILL_CATALOG.values():
        for skill in skills:
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                found_skills.add(normalize_skill(skill))

    return found_skills