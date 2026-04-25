from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.analyzer import extract_text, clean_words, calculate_ats_score


async def analyze_job_match(file, job_description: str):
    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "analysis_type": "job_match",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "experience_score": 0,
            "score_breakdown": {
                "semantic_match": 0,
                "skill_match": 0,
                "ats_score": 0,
                "experience_relevance": 0,
                "content_score": 0,
            },
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not extract text from resume."],
        }

    if not job_description or not job_description.strip():
        ats_score = calculate_ats_score(resume_text)

        return {
            "analysis_type": "job_match",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": ats_score,
            "experience_score": 0,
            "score_breakdown": {
                "semantic_match": 0,
                "skill_match": 0,
                "ats_score": ats_score,
                "experience_relevance": 0,
                "content_score": 0,
            },
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Job description is empty."],
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

    experience_keywords = [
        "experience", "internship", "intern", "worked",
        "developed", "built", "created", "implemented",
        "deployed", "optimized", "designed"
    ]

    experience_hits = sum(1 for word in experience_keywords if word in resume_lower)
    experience_score = min(100, experience_hits * 12)

    match_score = round(
        (raw_match_score * 0.35)
        + (skills_score * 0.25)
        + (ats_score * 0.20)
        + (experience_score * 0.10)
        + (content_score * 0.10),
        2,
    )

    if experience_score < 40:
        suggestions.append("Add more experience-focused points using action verbs like built, implemented, deployed, or optimized.")

    if match_score < 50:
        suggestions.append("Your resume is not well aligned with this role.")
    else:
        suggestions.append("Good alignment. Improve further with keywords.")

    return {
        "analysis_type": "job_match",
        "match_score": match_score,
        "skills_score": skills_score,
        "content_score": content_score,
        "ats_score": ats_score,
        "experience_score": experience_score,
        "score_breakdown": {
            "semantic_match": raw_match_score,
            "skill_match": skills_score,
            "ats_score": ats_score,
            "experience_relevance": experience_score,
            "content_score": content_score,
        },
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
    }