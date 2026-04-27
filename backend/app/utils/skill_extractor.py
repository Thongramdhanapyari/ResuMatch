from app.utils.skills_catalog import SKILL_CATALOG
from app.utils.skill_normalizer import normalize_skill


def extract_skills(text: str) -> set:
    text = text.lower()
    found_skills = set()

    for category, skills in SKILL_CATALOG.items():
        for skill in skills:
            if skill in text:
                found_skills.add(normalize_skill(skill))

    return found_skills