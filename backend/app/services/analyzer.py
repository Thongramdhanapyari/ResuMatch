STOPWORDS = {
    "the", "and", "with", "for", "you", "are", "this", "that",
    "from", "have", "has", "had", "was", "were", "will", "your",
    "using", "used", "use", "our", "their", "they", "them",
    "into", "onto", "also", "should", "can", "all", "any",
    "who", "how", "why", "get", "good", "strong", "required",
    "looking", "modern", "developer", "developers"
}


def clean_words(text: str) -> list[str]:
    if not text:
        return []

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
    if not resume_text:
        return 0

    text = resume_text.lower()
    word_count = len(resume_text.split())

    penalties = 0

    if "skills" not in text:
        penalties += 20

    if "education" not in text:
        penalties += 20

    if not any(k in text for k in ("project", "projects", "experience")):
        penalties += 20

    if word_count < 150:
        penalties += 20

    if "@" not in resume_text:
        penalties += 10

    return max(0, 100 - penalties)