import re

ACTION_VERBS = {
    "built", "developed", "created", "implemented", "designed",
    "optimized", "deployed", "improved", "managed", "led",
    "integrated", "automated", "engineered", "architected"
}


def check_email(text: str) -> bool:
    return bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text))


def check_phone(text: str) -> bool:
    return bool(re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text))


def check_links(text: str) -> dict:
    text_lower = text.lower()
    return {
        "github": "github.com" in text_lower,
        "linkedin": "linkedin.com" in text_lower
    }


def check_sections(text: str) -> dict:
    text_lower = text.lower()
    return {
        "skills": "skills" in text_lower,
        "education": "education" in text_lower,
        "projects": "project" in text_lower,
        "experience": "experience" in text_lower
    }


def check_bullet_quality(text: str) -> float:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return 0

    bullet_lines = sum(
        1 for line in lines
        if line.startswith(("•", "-", "*"))
    )

    return min(100, (bullet_lines / len(lines)) * 100)


def check_action_verbs(text: str) -> float:
    text_lower = text.lower()

    count = sum(
        text_lower.count(verb)
        for verb in ACTION_VERBS
    )

    return min(100, count * 8)


def check_length(text: str) -> float:
    words = len(text.split())

    if words < 120:
        return 40
    if words > 900:
        return 60
    return 100


def run_ats_checks(text: str):
    if not text:
        return {
            "ats_score": 0,
            "details": {}
        }

    email = check_email(text)
    phone = check_phone(text)
    links = check_links(text)
    sections = check_sections(text)

    bullet_score = check_bullet_quality(text)
    verb_score = check_action_verbs(text)
    length_score = check_length(text)

    score = 0

    score += 15 if email else 0
    score += 15 if phone else 0

    score += 10 if sections["skills"] else 0
    score += 10 if sections["education"] else 0
    score += 10 if sections["projects"] else 0
    score += 10 if sections["experience"] else 0

    score += 5 if links["github"] else 0
    score += 5 if links["linkedin"] else 0

    score += bullet_score * 0.1
    score += verb_score * 0.15
    score += length_score * 0.1

    return {
        "ats_score": round(min(100, score), 2),
        "details": {
            "email_present": email,
            "phone_present": phone,
            "links": links,
            "sections": sections,
            "bullet_score": round(bullet_score, 2),
            "action_verb_score": round(verb_score, 2),
            "length_score": length_score,
        }
    }