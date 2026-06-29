from pydantic import BaseModel, Field

class ResumeParseResponse(BaseModel):
    filename: str
    file_type: str
    extracted_text: str
    character_count: int
    is_scanned_pdf: bool = Field(
        default=False,
        description="True when PDF text extraction returned too little text, likely because the PDF is scanned/image-based."
    )
    message: str