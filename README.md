# AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions and provides a match score, missing skills, and improvement suggestions.

---

## 🚀 Features
- Upload PDF/DOCX resumes
- Compare with job description
- Match score calculation
- Missing & matched skills detection
- Smart suggestions for improvement
- Authentication (Signup/Login with JWT)

---

## 🛠️ Tech Stack
**Frontend**
- Next.js
- Tailwind CSS

**Backend**
- FastAPI
- SQLModel (SQLite)
- JWT Authentication

**AI / Processing**
- scikit-learn (cosine similarity)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)

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
SQLite is used for simplicity (can switch to PostgreSQL later)
```
### 👨‍💻 Author

AD