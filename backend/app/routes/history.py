from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from database import get_session
from app.models.analysis import AnalysisHistory
from app.core.security import verify_token

router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


@router.get("/history")
def get_analysis_history(
    job_title: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user")

    query = select(AnalysisHistory).where(AnalysisHistory.user_id == user_id)

    if job_title:
        query = query.where(AnalysisHistory.job_title.ilike(f"%{job_title}%"))

    if start_date:
        query = query.where(AnalysisHistory.created_at >= start_date)

    if end_date:
        query = query.where(AnalysisHistory.created_at <= end_date)

    query = query.order_by(AnalysisHistory.created_at.desc())

    return session.exec(query).all()