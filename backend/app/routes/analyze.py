from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from database import get_session
from app.core.security import verify_token
from app.services.job_match import analyze_job_match
from app.services.resume_quality import analyze_resume_quality
from app.services.history_service import save_analysis_history

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


def validate_pdf(resume: UploadFile):
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


@router.post("/analyze/job-match")
async def job_match(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    validate_pdf(resume)

    try:
        result = await analyze_job_match(resume, job_description)

        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User id not found in token")

        save_analysis_history(
            session=session,
            user_id=user_id,
            job_title=job_description[:80].strip() or "Untitled Role",
            resume_filename=resume.filename,
            result=result,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        print("JOB MATCH ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/resume-quality")
async def resume_quality(
    resume: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    validate_pdf(resume)

    try:
        result = await analyze_resume_quality(resume)

        user_id = current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User id not found in token")

        save_analysis_history(
            session=session,
            user_id=user_id,
            job_title="Resume Quality Analysis",
            resume_filename=resume.filename,
            result=result,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        print("RESUME QUALITY ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))