from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.analyzer import extract_text, calculate_ats_score
from app.utils.skill_extractor import extract_skills
from app.utils.section_parser import parse_sections
from app.utils.ats_checker import run_ats_checks

from sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


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

    try:
        resume_embedding = get_model().encode(resume_text)
        jd_embedding = get_model().encode(job_description)

        semantic_score = cosine_similarity(
            [resume_embedding],
            [jd_embedding]
        )[0][0]

        raw_match_score = round(float(semantic_score) * 100, 2)

    except Exception:
        raw_match_score = 0

    resume_lower = resume_text.lower()
    resume_skills = extract_skills(resume_text)
    parsed = parse_sections(resume_text)
    jd_skills = extract_skills(job_description)

    matched = list(resume_skills & jd_skills)
    missing = list(jd_skills - resume_skills)

    suggestions = []

    if missing:
        suggestions.append("Add missing relevant skills to your resume.")

    if "project" not in resume_lower and "projects" not in resume_lower:
        suggestions.append("Add a projects section to strengthen your resume.")

    if "skills" not in resume_lower:
        suggestions.append("Add a dedicated skills section for better ATS readability.")

    if len(resume_text.split()) < 150:
        suggestions.append("Your resume content looks short. Add more relevant details and impact.")

    if len(jd_skills) > 0:
        skills_score = round((len(matched) / len(jd_skills)) * 100, 2)
    else:
        skills_score = 0
        
    content_score = max(0, 100 - (len(suggestions) * 10))
    ats_result = run_ats_checks(resume_text)
    ats_score = ats_result["ats_score"]

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
        suggestions.append(
            "Add more experience-focused points using action verbs like built, implemented, deployed, or optimized."
        )

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
        "ats_details": ats_result["details"],
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
        "parsed_sections": parsed.get("sections", {}),
        "section_confidence": parsed.get("confidence", {}),
    }