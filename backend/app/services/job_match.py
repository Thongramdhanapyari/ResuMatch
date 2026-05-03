from app.utils.text_extractor import extract_text
from app.utils.skill_extractor import extract_skills
from app.utils.ats_checker import run_ats_checks
from app.utils.section_parser import parse_sections

from app.ml.job_match_engine import compute_job_match


async def analyze_job_match(file, job_description: str, session, user_id):

    resume_text = await extract_text(file)

    if not resume_text:
        return {
            "analysis_type": "job_match",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": 0,
            "experience_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Could not extract text from resume."],
        }

    if not job_description or not job_description.strip():
        ats_result = run_ats_checks(resume_text)

        return {
            "analysis_type": "job_match",
            "match_score": 0,
            "skills_score": 0,
            "content_score": 0,
            "ats_score": ats_result["ats_score"],
            "experience_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Job description is empty."],
        }

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    ats_result = run_ats_checks(resume_text)

    result = compute_job_match(
        resume_text,
        job_description,
        resume_skills,
        jd_skills,
        ats_result["ats_score"]
    )

    parsed = parse_sections(resume_text)

    result["analysis_type"] = "job_match"
    result["ats_score"] = ats_result["ats_score"]
    result["ats_details"] = ats_result["details"]
    result["parsed_sections"] = parsed.get("sections", {})
    result["section_confidence"] = {
        k: round(v * 100, 2)
        for k, v in parsed.get("confidence", {}).items()
    }

    return result