from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    # InterviewQuestion,
    # ResumeBulletRewrite,
)
from app.services.analysis_service import analyze_application

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job_application(payload: AnalyzeRequest) -> AnalyzeResponse:
    try:
        return analyze_application(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail = f"AI provider returned an invalid response: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail = f"Analysis failed: {str(exc)}",
        ) from exc