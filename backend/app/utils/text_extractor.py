import pdfplumber
from docx import Document
import io


async def extract_text(file) -> str:
    filename = file.filename.lower()

    content = await file.read()

    # PDF
    if filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    # DOCX
    if filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    # fallback
    return content.decode(errors="ignore")