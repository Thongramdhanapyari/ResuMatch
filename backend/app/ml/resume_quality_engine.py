WEAK_WORDS = [
    "hardworking", "passionate", "good", "nice", "responsible",
    "team player", "quick learner"
]

ACTION_WORDS = [
    "built", "developed", "created", "implemented", "designed",
    "optimized", "deployed", "improved", "managed", "led",
    "integrated", "automated"
]

COMMON_SECTIONS = [
    "skills", "education", "projects", "experience",
    "summary", "certifications"
]


def compute_spelling_score(words: list) -> tuple[int, list]:
    issues = []

    for word in words:
        clean = word.strip(".,()[]{}:-").lower()
        if not clean.isalpha() or len(clean) > 15:
            issues.append(clean)

    issues = list(set(issues))[:10]
    score = max(0, 100 - len(issues) * 5)

    return score, issues


def compute_semantic_score(resume_text: str) -> tuple[int, list]:
    suggestions = []
    text_lower = resume_text.lower()

    score = 100

    if not any(word in text_lower for word in ACTION_WORDS):
        score -= 20
        suggestions.append("Use strong action verbs like built, developed, or implemented.")

    if "project" not in text_lower:
        score -= 15
        suggestions.append("Add a projects section.")

    if "experience" not in text_lower:
        score -= 15
        suggestions.append("Add an experience section.")

    if not any(char.isdigit() for char in resume_text):
        score -= 20
        suggestions.append("Add measurable impact like improved performance by 30% or handled 100+ users.")

    return max(0, score), suggestions


def compute_content_score(suggestions: list) -> int:
    return max(0, 100 - len(suggestions) * 8)