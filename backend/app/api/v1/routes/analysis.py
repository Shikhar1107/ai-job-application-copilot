from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
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
from app.db.session import get_db
from app.services.history_service import (
    save_analysis_run,
    update_analysis_rewritten_bullets,
    update_analysis_cover_letter,
    update_analysis_interview_questions,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job_application(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
) -> AnalyzeResponse:
    try:
        response = analyze_application(payload)

        saved_run = save_analysis_run(
            db=db,
            request_payload=payload,
            response_payload=response,
        )

        response.analysis_id = saved_run.id

        return response

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider returned an invalid response: {str(exc)}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(exc)}",
        ) from exc
    

@router.post("/rewrite-bullets", response_model=RewriteBulletsResponse)
def rewrite_bullets(
    payload: RewriteBulletsRequest,
    db: Session = Depends(get_db),
) -> RewriteBulletsResponse:
    try:
        response = generate_resume_rewrites(payload)

        if payload.analysis_id is not None:
            updated = update_analysis_rewritten_bullets(
                db=db,
                analysis_id=payload.analysis_id,
                rewritten_bullets=response.rewritten_bullets,
            )

            if updated is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Analysis with id {payload.analysis_id} not found",
                )

        return response

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider returned an invalid response: {str(exc)}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume rewrite failed: {str(exc)}",
        ) from exc
    

@router.post("/cover-letter", response_model=CoverLetterResponse)
def cover_letter(
    payload: CoverLetterRequest,
    db: Session = Depends(get_db),
) -> CoverLetterResponse:
    try:
        response = generate_tailored_cover_letter(payload)

        if payload.analysis_id is not None:
            updated = update_analysis_cover_letter(
                db=db,
                analysis_id=payload.analysis_id,
                cover_letter=response.cover_letter,
            )

            if updated is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Analysis with id {payload.analysis_id} not found",
                )

        return response

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider returned an invalid response: {str(exc)}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cover letter generation failed: {str(exc)}",
        ) from exc

@router.post("/interview-questions", response_model=InterviewQuestionsResponse)
def interview_questions(
    payload: InterviewQuestionsRequest,
    db: Session = Depends(get_db),
) -> InterviewQuestionsResponse:
    try:
        response = generate_tailored_interview_questions(payload)

        if payload.analysis_id is not None:
            updated = update_analysis_interview_questions(
                db=db,
                analysis_id=payload.analysis_id,
                interview_questions=response.interview_questions,
            )

            if updated is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Analysis with id {payload.analysis_id} not found",
                )

        return response

    except HTTPException:
        raise

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