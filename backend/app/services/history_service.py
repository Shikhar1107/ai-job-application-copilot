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
        rewritten_bullets=serialize_pydantic_list(response_payload.rewritten_bullets) or [],
        cover_letter=response_payload.cover_letter or "",
        interview_questions=serialize_pydantic_list(response_payload.interview_questions) or [],
    )

    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    return analysis_run

def update_analysis_rewritten_bullets(
    db: Session,
    analysis_id: int,
    rewritten_bullets: list[dict],
) -> AnalysisRun | None:
    analysis_run = get_analysis_by_id(db, analysis_id)

    if analysis_run is None:
        return None

    analysis_run.rewritten_bullets = serialize_pydantic_list(rewritten_bullets)
    db.commit()
    db.refresh(analysis_run)

    return analysis_run


def update_analysis_cover_letter(
    db: Session,
    analysis_id: int,
    cover_letter: str,
) -> AnalysisRun | None:
    analysis_run = get_analysis_by_id(db, analysis_id)

    if analysis_run is None:
        return None

    analysis_run.cover_letter = cover_letter
    db.commit()
    db.refresh(analysis_run)

    return analysis_run


def update_analysis_interview_questions(
    db: Session,
    analysis_id: int,
    interview_questions: list[dict],
) -> AnalysisRun | None:
    analysis_run = get_analysis_by_id(db, analysis_id)

    if analysis_run is None:
        return None

    analysis_run.interview_questions =  serialize_pydantic_list(interview_questions)
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

def serialize_pydantic_list(items: list) -> list[dict]:
    serialized = []

    for item in items or []:
        if hasattr(item, "model_dump"):
            serialized.append(item.model_dump())
        elif isinstance(item, dict):
            serialized.append(item)
        else:
            serialized.append(dict(item))

    return serialized

def delete_analysis_by_id(db: Session, analysis_id: int) -> bool:
    analysis_run = get_analysis_by_id(db, analysis_id)

    if analysis_run is None:
        return False

    db.delete(analysis_run)
    db.commit()

    return True