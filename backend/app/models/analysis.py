from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class AnalysisHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    job_title: str = Field(index=True)
    resume_filename: str

    analysis_type: str = "job_match"          # NEW
    experience_score: float = 0               # NEW

    match_score: float
    skills_score: float
    content_score: float
    ats_score: float

    matched_skills: str
    missing_skills: str
    suggestions: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )