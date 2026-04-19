from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.parser import extract_text

STOPWORDS = {
    "the", "and", "with", "for", "you", "are", "this", "that",
    "from", "have", "has", "had", "was", "were", "will", "your",
    "using", "used", "use", "our", "their", "they", "them",
    "into", "onto", "also", "should", "can", "all", "any",
    "who", "how", "why", "get", "good", "strong", "required",
    "looking", "modern", "developer", "developers"
}

def clean_words(text):
    words = text.lower().split()
    cleaned = []
    seen = set()

    for w in words:
        word = w.strip(".,()[]{}:-")
        if len(word) > 2 and word not in STOPWORDS and word not in seen:
            cleaned.append(word)
            seen.add(word)

    return cleaned


def calculate_ats_score(resume_text):
    ats_score = 100
    resume_lower = resume_text.lower()

    if "skills" not in resume_lower:
        ats_score -= 20
    if "education" not in resume_lower:
        ats_score -= 20
    if "project" not in resume_lower and "projects" not in resume_lower and "experience" not in resume_lower:
        ats_score -= 20
    if len(resume_text.split()) < 150:
        ats_score -= 20
    if "@" not in resume_text:
        ats_score -= 10

    return max(0, ats_score)


async def analyze_resume(file, job_description):
    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not read resume properly"],
        }

    if not job_description or not job_description.strip():
        return {
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Job description is empty"],
        }

    texts = [resume_text, job_description]

    try:
        vectorizer = TfidfVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    except Exception:
        score = 0

    resume_lower = resume_text.lower()
    resume_words = set(clean_words(resume_text))
    jd_words = clean_words(job_description)

    matched = [w for w in jd_words if w in resume_words][:15]
    missing = [w for w in jd_words if w not in resume_words][:15]

    suggestions = []

    if missing:
        suggestions.append("Add missing relevant skills to your resume.")

    if "project" not in resume_lower and "projects" not in resume_lower:
        suggestions.append("Add a projects section to strengthen your resume.")

    if "skills" not in resume_lower:
        suggestions.append("Add a dedicated skills section for better ATS readability.")

    if len(resume_text.split()) < 150:
        suggestions.append("Your resume content looks short. Add more relevant details and impact.")

    raw_match_score = round(score * 100, 2)

    total_skills = len(matched) + len(missing)
    skills_score = round((len(matched) / total_skills) * 100, 2) if total_skills > 0 else 0

    content_score = max(0, 100 - (len(suggestions) * 10))
    ats_score = calculate_ats_score(resume_text)

    match_score = round(
        (raw_match_score * 0.4) +
        (skills_score * 0.3) +
        (content_score * 0.15) +
        (ats_score * 0.15),
        2
    )

    if match_score < 50:
        suggestions.append("Your resume is not well aligned with this role.")
    else:
        suggestions.append("Good alignment. Improve further with keywords.")

    return {
        "match_score": match_score,
        "skills_score": skills_score,
        "content_score": content_score,
        "ats_score": ats_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
    }