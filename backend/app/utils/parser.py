import os
import uuid
import fitz  # PyMuPDF
from docx import Document

TEMP_DIR = os.getenv("TEMP_DIR", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


async def extract_text(file):
    if not file or not file.filename:
        return ""

    filename = file.filename.lower()
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{filename}")

    try:
        with open(temp_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)

        parts = []

        if filename.endswith(".pdf"):
            doc = fitz.open(temp_path)
            try:
                for page in doc:
                    text = page.get_text()
                    if text:
                        parts.append(text)
            finally:
                doc.close()

        elif filename.endswith(".docx"):
            doc = Document(temp_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    parts.append(para.text)

        else:
            return ""

        return " ".join(parts).strip()

    except Exception:
        return ""

    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass