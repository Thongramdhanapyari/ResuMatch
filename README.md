# AI Resume Analyzer

An AI-powered web application that analyzes resumes using semantic NLP, rule-based ATS evaluation, and structured document understanding to provide job match scores, resume quality scores, skill gaps, and improvement suggestions.

---

## 🚀 Features

### 📄 Resume Analysis
- Upload PDF/DOCX resumes
- Resume quality scoring (ATS + structure + semantic + spelling)
- Section detection (skills, projects, experience, education, summary)
- Action verb & formatting evaluation
- Spelling and content quality checks

### 🎯 Job Matching (AI-Powered)
- Resume vs Job Description similarity using TF-IDF + cosine similarity
- Skill extraction with normalization (aliases like js → javascript)
- Matched & missing skills detection
- Experience relevance scoring
- ATS compatibility score

### 🧠 AI Intelligence Layer
- Lightweight NLP pipeline using TF-IDF (optimized for low-memory environments)
- Hybrid scoring system (rules + statistical NLP)
- Structured score breakdown:
  - Semantic match
  - Skill match
  - ATS score
  - Experience relevance
  - Content quality

### 🔐 Authentication
- JWT-based login/signup system
- Protected analysis routes

---

## 🛠️ Tech Stack

### Frontend
- Next.js (App Router)
- Tailwind CSS
- jsPDF (report export)

### Backend
- FastAPI
- SQLModel (PostgreSQL ready, SQLite for dev)
- JWT Authentication

### NLP Engine
- scikit-learn (TF-IDF + cosine similarity)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)

### Core Modules
- Skill extraction engine (normalized skill catalog)
- Section parser (regex + heading detection)
- ATS rule-based evaluator
- Resume–JD similarity using TF-IDF

---

## ⚙️ Setup (Local)

### 1. Clone repo
```bash
git clone <your-repo-link>
cd project
``` 

### 2. Backend setup
``` bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Create .env:
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your_secret
FRONTEND_URL=http://localhost:3000
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev

Create .env.local:
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```
## 🌐 Deployment
```bash
Backend (Render)
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
Frontend (Vercel)

Switch to PostgreSQL in production:

DATABASE_URL=postgresql://user:password@host/db

Add env:
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## 🔐 Environment Variables
### Backend
```bash
DATABASE_URL
SECRET_KEY
FRONTEND_URL 
```
### Frontend
```bash
NEXT_PUBLIC_API_URL
```

## ⚠️ Notes
```bash
Do not commit .env or .env.local
temp/ folder is auto-generated
SQLite is used for development; PostgreSQL recommended for production
```
### 👨‍💻 Author

AD