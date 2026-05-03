from sqlmodel import Session, select
from app.models.user import User


def get_user_by_email(session: Session, email: str):
    return session.exec(
        select(User).where(User.email == email)
    ).first()


def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user