ALIASES = {
    "js": "javascript",
    "node": "node.js",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "postgres db": "postgresql",
    "reactjs": "react",
    "ml": "machine learning",
    "ds": "data structures",
    "algo": "algorithms"
}


def normalize_skill(skill: str) -> str:
    if not skill:
        return ""

    skill = skill.lower().strip()
    skill = " ".join(skill.split())

    return ALIASES.get(skill, skill)