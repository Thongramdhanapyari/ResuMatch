from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database import engine
from app.routes.analyze import router as analyze_router
from app.routes.auth import router as auth_router
from app.routes.history import router as history_router

from app.models.user import User
from app.models.analysis import AnalysisHistory

app = FastAPI(title="ResuMatch API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://resu-match-psi.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(analyze_router, prefix="/api", tags=["Analyze"])
app.include_router(history_router, prefix="/api", tags=["History"])


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}