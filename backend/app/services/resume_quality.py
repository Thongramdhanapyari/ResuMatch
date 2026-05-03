from app.utils.text_extractor import extract_text
from app.utils.skill_extractor import extract_skills
from app.utils.section_parser import parse_sections
from app.utils.ats_checker import run_ats_checks
from app.utils.bullet_analyzer import analyze_bullets

from app.ml.resume_quality_engine import (
    compute_spelling_score,
    compute_semantic_score,
    compute_content_score,
    WEAK_WORDS,
    COMMON_SECTIONS
)


async def analyze_resume_quality(file):
    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "analysis_type": "resume_quality",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "semantic_score": 0,
            "spelling_score": 0,
            "matched_skills": [],
            "suggestions": ["Could not extract text from resume."],
            "parsed_sections": {},
            "section_confidence": {},
            "ats_details": {},
            "bullet_score": 0,
            "bullet_analysis": [],
        }

    resume_lower = resume_text.lower()
    words = resume_text.split()
    word_count = len(words)

    parsed = parse_sections(resume_text)
    ats_result = run_ats_checks(resume_text)
    bullet_result = analyze_bullets(resume_text)

    bullet_score = bullet_result["bullet_score"]
    bullet_analysis = bullet_result["analysis"]

    suggestions = []

    missing_sections = [
        section for section in COMMON_SECTIONS
        if section not in resume_lower
    ]

    if missing_sections:
        suggestions.append("Missing sections: " + ", ".join(missing_sections))

    if word_count < 150:
        suggestions.append("Resume is too short. Add more impact and details.")
    elif word_count > 900:
        suggestions.append("Resume may be too long. Keep it concise.")

    if "@" not in resume_text:
        suggestions.append("Add a professional email address.")

    weak_found = [word for word in WEAK_WORDS if word in resume_lower]
    if weak_found:
        suggestions.append("Avoid weak words: " + ", ".join(weak_found))

    spelling_score, _ = compute_spelling_score(words)

    semantic_score, semantic_suggestions = compute_semantic_score(resume_text)
    suggestions.extend(semantic_suggestions)

    resume_skills = extract_skills(resume_text)
    skills_score = min(100, len(resume_skills) * 4)

    if skills_score < 40:
        suggestions.append("Add more relevant technical skills.")

    content_score = compute_content_score(suggestions)

    ats_score = ats_result["ats_score"]

    final_score = round(
        (ats_score * 0.28)
        + (semantic_score * 0.28)
        + (spelling_score * 0.14)
        + (content_score * 0.20)
        + (bullet_score * 0.10),
        2
    )

    suggestions = list(dict.fromkeys(suggestions))

    return {
        "analysis_type": "resume_quality",
        "match_score": final_score,
        "skills_score": skills_score,
        "content_score": content_score,
        "ats_score": ats_score,
        "semantic_score": semantic_score,
        "spelling_score": spelling_score,
        "score_breakdown": {
            "ats_score": ats_score,
            "semantic_strength": semantic_score,
            "spelling_quality": spelling_score,
            "content_quality": content_score,
            "bullet_quality": bullet_score,
        },
        "matched_skills": list(resume_skills),
        "suggestions": suggestions or [
            "Resume looks strong. Improve further with better metrics and impact."
        ],
        "parsed_sections": parsed.get("sections", {}),
        "section_confidence": {
            k: round(v * 100, 2)
            for k, v in parsed.get("confidence", {}).items()
        },
        "ats_details": ats_result["details"],
        "bullet_score": bullet_score,
        "bullet_analysis": bullet_analysis,
    }