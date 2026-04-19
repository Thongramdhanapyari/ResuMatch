from pydantic import BaseModel, EmailStr, Field

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut