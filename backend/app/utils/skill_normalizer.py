ALIASES = {
    "js": "javascript",
    "node": "node.js",
    "postgres": "postgresql",
    "postgres db": "postgresql",
    "reactjs": "react",
    "ml": "machine learning",
    "ds": "data structures",
    "algo": "algorithms"
}


def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return ALIASES.get(skill, skill)