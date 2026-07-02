from fastapi import File, APIRouter, HTTPException, UploadFile

from app.schemas.resume import ResumeParseResponse
from app.services.resume_parser import UnsupportedFileTypeError, parse_resume_file

router = APIRouter(prefix="/resume",tags=["Resume"])

@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(
    file: UploadFile = File(...),
) -> ResumeParseResponse:
    try:
        result = await parse_resume_file(file)
        return ResumeParseResponse(**result)
    
    except UnsupportedFileTypeError as exc:
        raise HTTPException(
            status_code=400,
            detail = str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail = f"Resume parsing failed: {str(exc)}",
        ) from exc

