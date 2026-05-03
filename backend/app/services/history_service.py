import json
from sqlmodel import Session
from app.models.analysis import AnalysisHistory


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def save_analysis_history(
    session: Session,
    user_id: int,
    job_title: str,
    resume_filename: str,
    result: dict,
) -> AnalysisHistory:

    analysis_type = result.get("analysis_type", "job_match")

    history = AnalysisHistory(
        user_id=user_id,
        job_title=(job_title or "Untitled").strip(),
        resume_filename=resume_filename,

        analysis_type=analysis_type,
        experience_score=safe_float(result.get("experience_score")),

        match_score=safe_float(result.get("match_score")),
        skills_score=safe_float(result.get("skills_score")),
        content_score=safe_float(result.get("content_score")),
        ats_score=safe_float(result.get("ats_score")),

        matched_skills=json.dumps(result.get("matched_skills") or []),

        missing_skills=json.dumps(
            result.get("missing_skills") or []
            if analysis_type == "job_match"
            else []
        ),

        suggestions=json.dumps(result.get("suggestions") or []),
    )

    try:
        session.add(history)
        session.commit()
        session.refresh(history)
        return history

    except Exception:
        session.rollback()
        raise