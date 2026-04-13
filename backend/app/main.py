from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router
from app.routes.auth import router as auth_router
from sqlmodel import SQLModel
from database import engine
import os

app = FastAPI()

SQLModel.metadata.create_all(engine)

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
    allow_credentials=False if FRONTEND_URL == "*" else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
def root():
    return {"message": "Backend running"}