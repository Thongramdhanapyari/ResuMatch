from sqlmodel import Session, select
from app.models.analysis import AnalysisHistory


def save_analysis(session: Session, obj: AnalysisHistory):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_user_history(session: Session, user_id: int):
    query = select(AnalysisHistory).where(
        AnalysisHistory.user_id == user_id
    )
    return session.exec(query).all()