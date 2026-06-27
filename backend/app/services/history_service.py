from sqlalchemy.orm import Session

from app.db.models import AnalysisRun
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse


def save_analysis_run(
    db: Session,
    request_payload: AnalyzeRequest,
    response_payload: AnalyzeResponse,
) -> AnalysisRun:
    analysis_run = AnalysisRun(
        resume_text=request_payload.resume_text,
        job_description=request_payload.job_description,
        fit_score=response_payload.fit_score,
        fit_summary=response_payload.fit_summary,
        resume_skills=response_payload.resume_skills,
        job_required_skills=response_payload.job_required_skills,
        matched_skills=response_payload.matched_skills,
        missing_skills=response_payload.missing_skills,
        rewritten_bullets=[
            item.model_dump() for item in response_payload.rewritten_bullets
        ],
        cover_letter=response_payload.cover_letter,
        interview_questions=[
            item.model_dump() for item in response_payload.interview_questions
        ],
    )

    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    return analysis_run


def get_analysis_history(db: Session) -> list[AnalysisRun]:
    return (
        db.query(AnalysisRun)
        .order_by(AnalysisRun.created_at.desc())
        .all()
    )


def get_analysis_by_id(db: Session, analysis_id: int) -> AnalysisRun | None:
    return (
        db.query(AnalysisRun)
        .filter(AnalysisRun.id == analysis_id)
        .first()
    )