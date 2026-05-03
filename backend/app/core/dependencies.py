from app.core.security import verify_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(401, "Invalid token")

    return payload