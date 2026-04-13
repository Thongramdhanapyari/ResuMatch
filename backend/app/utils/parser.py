import os
import uuid
import fitz  # PyMuPDF
from docx import Document

TEMP_DIR = os.getenv("TEMP_DIR", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


async def extract_text(file):
    filename = file.filename.lower()
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{filename}")

    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    text = ""

    try:
        if filename.endswith(".pdf"):
            doc = fitz.open(temp_path)
            try:
                for page in doc:
                    text += page.get_text()
            finally:
                doc.close()

        elif filename.endswith(".docx"):
            doc = Document(temp_path)
            for para in doc.paragraphs:
                text += para.text + " "

        else:
            return ""

    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                pass

    return text.strip()