from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


def get_user_by_email(session: Session, email: str):
    return session.exec(
        select(User).where(User.email == email)
    ).first()


def generate_user_response(user: User):
    token = create_access_token(
        {"sub": user.email, "id": user.id}
    )

    return {
        "message": "Success",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/signup")
def signup(data: UserCreate, session: Session = Depends(get_session)):
    email = data.email.lower().strip()

    if get_user_by_email(session, email):
        raise HTTPException(status_code=400, detail="Email already exists")

    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")

    user = User(
        name=data.name.strip(),
        email=email,
        hashed_password=hash_password(data.password),
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Signup failed")

    return generate_user_response(user)


@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    email = data.email.lower().strip()

    user = get_user_by_email(session, email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return generate_user_response(user)