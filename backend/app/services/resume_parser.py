from pathlib import Path

import fitz
from docx import Document
from fastapi import UploadFile

MIN_EXTRACTED_TEXT_LENGTH = 200

class UnsupportedFileTypeError(ValueError):
    pass

class ScannedPDFError(ValueError):
    pass

async def parse_resume_file(file: UploadFile) -> dict:
    filename = file.filename or "uploaded_resume"
    extension = Path(filename).suffix.lower()

    file_bytes = await file.read()

    if extension == ".pdf":
        extraced_text = _extract_text_from_pdf(file_bytes)
        is_scanned_pdf = len(extraced_text.strip()) < MIN_EXTRACTED_TEXT_LENGTH

        if is_scanned_pdf:
            return {
                "filename": filename,
                "file_type": "pdf",
                "character_count": len(extraced_text),
                "is_scanned_pdf": True,
                "message": (
                    "This PDF appears to be scanned or image-based. "
                    "Text extraction returned very little text. OCR support will be needed for this file "
                ),
            }
    
        return {
            "filename": filename,
            "file_type": "pdf",
            "extracted_text": extraced_text,
            "character_count": len(extraced_text),
            "is_scanned_pdf": False,
            "message" : "Resume text extracted successfully from PDF.",
        }
    
    if extension == ".docx":
        extracted_text = _extract_text_from_docx(file_bytes)

        return {
            "filename": filename,
            "file_type": "docx",
            "extracted_text": extracted_text,
            "character_count": len(extracted_text),
            "is_scanned_pdf": False,
            "message": "Resume text extracted successfully from DOCX.",
        }

    if extension == ".txt":
        extracted_text = _extract_text_from_txt(file_bytes)

        return {
            "filename": filename,
            "file_type": "txt",
            "extracted_text": extracted_text,
            "character_count": len(extracted_text),
            "is_scanned_pdf": False,
            "message": "Resume text extracted successfully from TXT.",
        }

    raise UnsupportedFileTypeError(
        "Unsupported file type. Please upload a PDF, DOCX, or TXT resume."
    )


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts: list[str] = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def _extract_text_from_docx(file_bytes: bytes) -> str:
    from io import BytesIO

    document = Document(BytesIO(file_bytes))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def _extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8").strip()
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1").strip()