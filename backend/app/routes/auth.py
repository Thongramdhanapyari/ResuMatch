from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup")
def signup(data: UserCreate, session: Session = Depends(get_session)):
    email = data.email.lower().strip()

    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = User(
        name=data.name.strip(),
        email=email,
        password=hash_password(data.password),
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Signup failed")

    token = create_access_token(
        {"sub": user.email, "id": user.id}
    )

    return {
        "message": "Signup successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    email = data.email.lower().strip()

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {"sub": user.email, "id": user.id}
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }