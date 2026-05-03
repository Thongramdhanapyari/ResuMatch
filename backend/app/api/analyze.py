from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlmodel import Session

from database import get_session
from app.core.dependencies import get_current_user
from app.services.job_match_orchestrator import analyze_job_match_service

router = APIRouter()


@router.post("/job-match")
async def job_match(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    return await analyze_job_match_service(
        resume,
        job_description,
        session,
        current_user["id"]
    )