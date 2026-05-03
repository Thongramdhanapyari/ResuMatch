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
    payload = verify_token(credentials.credentials)

    if not payload or not payload.get("id"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


def validate_pdf(resume: UploadFile):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")


def get_user_id(current_user: dict) -> int:
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User id not found in token")
    return user_id


@router.post("/analyze/job-match")
async def job_match(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    validate_pdf(resume)

    try:
        result = await analyze_job_match(
            resume,
            job_description,
            session,
            get_user_id(current_user)
        )
        save_analysis_history(
            session=session,
            user_id=get_user_id(current_user),
            job_title=job_description[:80].strip() or "Untitled Role",
            resume_filename=resume.filename,
            result=result,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"[JOB MATCH ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/analyze/resume-quality")
async def resume_quality(
    resume: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    validate_pdf(resume)

    try:
        result = await analyze_resume_quality(resume)

        save_analysis_history(
            session=session,
            user_id=get_user_id(current_user),
            job_title="Resume Quality Analysis",
            resume_filename=resume.filename,
            result=result,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"[RESUME QUALITY ERROR] {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")