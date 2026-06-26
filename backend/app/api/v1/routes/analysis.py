from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    RewriteBulletsRequest,
    RewriteBulletsResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
    # ResumeBulletRewrite,
)
from app.services.analysis_service import analyze_application, generate_tailored_cover_letter, generate_resume_rewrites, generate_tailored_interview_questions

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
    
@router.post("/rewrite-bullets",response_model=RewriteBulletsResponse)
def rewrite_bullets(payload: RewriteBulletsRequest) -> RewriteBulletsResponse:
    try:
        return generate_resume_rewrites(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail = f"AI provider returned an invalid response: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail = f"Resume rewrite failed: {str(exc)}",
        ) from exc

@router.post("/cover-letter", response_model=CoverLetterResponse)
def cover_letter(payload: CoverLetterRequest) -> CoverLetterResponse:
    try:
        return generate_tailored_cover_letter(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail = f"AI provider returned an invalid response: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail = f"Cover letter generation failed: {str(exc)}",
        ) from exc
    
@router.post("/interview-questions", response_model=InterviewQuestionsResponse)
def interview_questions(
    payload: InterviewQuestionsRequest
) -> InterviewQuestionsResponse:
    try:
        return generate_tailored_interview_questions(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider returned an invalid response: {str(exc)}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Interview question generation failed: {str(exc)}",
        ) from exc