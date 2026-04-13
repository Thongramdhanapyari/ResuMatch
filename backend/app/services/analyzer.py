from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.parser import extract_text

def clean_words(text):
    words = text.lower().split()
    return list(set([w.strip(".,()[]{}:-") for w in words if len(w) > 2]))

async def analyze_resume(file, job_description):
    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not read resume properly"]
        }

    texts = [resume_text, job_description]

    try:
        vectorizer = CountVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    except Exception:
        score = 0

    match_score = round(score * 100, 2)

    resume_words = clean_words(resume_text)
    jd_words = clean_words(job_description)

    matched = [w for w in jd_words if w in resume_words][:15]
    missing = [w for w in jd_words if w not in resume_words][:15]

    suggestions = []
    if missing:
        suggestions.append("Add missing relevant skills to your resume.")
    if match_score < 50:
        suggestions.append("Your resume is not well aligned with this role.")
    else:
        suggestions.append("Good alignment. Improve further with keywords.")

    return {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }