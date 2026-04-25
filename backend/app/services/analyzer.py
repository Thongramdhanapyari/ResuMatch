from app.utils.parser import extract_text

STOPWORDS = {
    "the", "and", "with", "for", "you", "are", "this", "that",
    "from", "have", "has", "had", "was", "were", "will", "your",
    "using", "used", "use", "our", "their", "they", "them",
    "into", "onto", "also", "should", "can", "all", "any",
    "who", "how", "why", "get", "good", "strong", "required",
    "looking", "modern", "developer", "developers"
}


def clean_words(text: str) -> list[str]:
    words = text.lower().split()
    cleaned = []
    seen = set()

    for w in words:
        word = w.strip(".,()[]{}:-")
        if len(word) > 2 and word not in STOPWORDS and word not in seen:
            cleaned.append(word)
            seen.add(word)

    return cleaned


def calculate_ats_score(resume_text: str) -> int:
    ats_score = 100
    resume_lower = resume_text.lower()

    if "skills" not in resume_lower:
        ats_score -= 20
    if "education" not in resume_lower:
        ats_score -= 20
    if (
        "project" not in resume_lower
        and "projects" not in resume_lower
        and "experience" not in resume_lower
    ):
        ats_score -= 20
    if len(resume_text.split()) < 150:
        ats_score -= 20
    if "@" not in resume_text:
        ats_score -= 10

    return max(0, ats_score)