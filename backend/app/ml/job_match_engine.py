from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def compute_semantic_score(resume_text: str, job_description: str) -> float:
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        vectors = vectorizer.fit_transform([resume_text, job_description])
        tfidf_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        model = get_model()
        embeddings = model.encode([resume_text[:2000], job_description[:2000]])

        bert_score = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        score = (0.6 * bert_score) + (0.4 * tfidf_score)
        score = (score + 1) / 2

        return round(score * 100, 2)

    except Exception:
        return 0


def compute_experience_score(resume_text: str) -> int:
    text = resume_text.lower()

    keywords = [
        "experience", "internship", "intern", "worked",
        "developed", "built", "created", "implemented",
        "deployed", "optimized", "designed"
    ]

    hits = sum(text.count(word) for word in keywords)
    return min(100, hits * 8)


def compute_content_score(resume_text: str):
    suggestions = []
    text = resume_text.lower()

    if "project" not in text:
        suggestions.append("Add a projects section.")

    if "skills" not in text:
        suggestions.append("Add a skills section.")

    if len(resume_text.split()) < 150:
        suggestions.append("Add more content with measurable impact.")

    score = max(0, 100 - len(suggestions) * 10)

    return score, suggestions


def compute_job_match(resume_text: str, job_description: str, resume_skills, jd_skills, ats_score):
    semantic_score = compute_semantic_score(resume_text, job_description)

    matched = list(resume_skills & jd_skills)
    missing = list(jd_skills - resume_skills)

    skills_score = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0

    experience_score = compute_experience_score(resume_text)

    content_score, suggestions = compute_content_score(resume_text)

    match_score = round(
        (semantic_score * 0.35)
        + (skills_score * 0.25)
        + (ats_score * 0.20)
        + (experience_score * 0.10)
        + (content_score * 0.10),
        2,
    )

    return {
        "match_score": match_score,
        "skills_score": skills_score,
        "content_score": content_score,
        "experience_score": experience_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "score_breakdown": {
            "semantic_match": semantic_score,
            "skill_match": skills_score,
            "ats_score": ats_score,
            "experience_relevance": experience_score,
            "content_score": content_score,
        },
    }