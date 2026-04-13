from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup")
def signup(data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        name=data.name,
        email=data.email.lower().strip(),
        password=hash_password(data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(
        {"sub": user.email, "id": user.id, "name": user.name}
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
    user = session.exec(
        select(User).where(User.email == data.email.lower().strip())
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {"sub": user.email, "id": user.id, "name": user.name}
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