from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router
from app.routes.auth import router as auth_router
from sqlmodel import SQLModel
from database import engine

app = FastAPI()

SQLModel.metadata.create_all(engine)

origins = [
    "http://localhost:3000",
    "https://resu-match-psi.vercel.app",
    "https://resu-match-c7qk4tygu-thongramdhanapyaris-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")


@app.get("/")
def root():
    return {
        "message": "Backend running",
        "cors_version": "main.py with psi vercel origin"
    }