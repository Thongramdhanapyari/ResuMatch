import json
from sqlmodel import Session
from app.models.analysis import AnalysisHistory


def save_analysis_history(
    session: Session,
    user_id: int,
    job_title: str,
    resume_filename: str,
    result: dict,
) -> AnalysisHistory:
    history = AnalysisHistory(
        user_id=user_id,
        job_title=job_title,
        resume_filename=resume_filename,

        analysis_type=result.get("analysis_type", "job_match"),   # NEW
        experience_score=float(result.get("experience_score", 0)),# NEW

        match_score=float(result.get("match_score", 0)),
        skills_score=float(result.get("skills_score", 0)),
        content_score=float(result.get("content_score", 0)),
        ats_score=float(result.get("ats_score", 0)),

        matched_skills=json.dumps(result.get("matched_skills", [])),
        missing_skills=json.dumps(result.get("missing_skills", [])),
        suggestions=json.dumps(result.get("suggestions", [])),
    )

    session.add(history)
    session.commit()
    session.refresh(history)
    return history