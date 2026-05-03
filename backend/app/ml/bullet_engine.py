import re

ACTION_VERBS = {
    "built", "developed", "created", "implemented", "designed",
    "optimized", "deployed", "improved", "managed", "led",
    "integrated", "automated", "engineered", "architected"
}

TECH_STACK = {
    "python", "javascript", "java", "react", "fastapi", "django",
    "node", "docker", "kubernetes", "aws", "gcp",
    "mongodb", "postgresql", "sql", "jwt", "api"
}

VAGUE_PHRASES = {
    "worked on", "responsible for", "handled",
    "did", "helped with", "assisted in", "involved in"
}


def analyze_bullet(bullet: str) -> dict:
    text = bullet.lower().strip()

    starts_with_action = any(text.startswith(v) for v in ACTION_VERBS)
    contains_tech = any(t in text for t in TECH_STACK)

    has_outcome = bool(
        re.search(r"\d+|%|improved|reduced|increased|decreased", text)
    )

    is_too_short = len(bullet.split()) < 6
    is_vague = any(v in text for v in VAGUE_PHRASES)

    score = (
        int(starts_with_action) * 20 +
        int(contains_tech) * 20 +
        int(has_outcome) * 30 +
        int(not is_too_short) * 15 +
        int(not is_vague) * 15
    )

    return {
        "bullet": bullet,
        "starts_with_action": starts_with_action,
        "contains_tech": contains_tech,
        "has_outcome": has_outcome,
        "too_short": is_too_short,
        "vague": is_vague,
        "score": score
    }


def extract_bullets(text: str) -> list[str]:
    lines = re.split(r"\n|•|- |\d+\.", text)
    return [
        line.strip()
        for line in lines
        if len(line.strip()) > 10
    ]