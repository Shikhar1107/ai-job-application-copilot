from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)

    fit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    fit_summary: Mapped[str] = mapped_column(Text, nullable=False)

    resume_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    job_required_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    matched_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    missing_skills: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    cover_letter: Mapped[str] = mapped_column(Text, nullable=True)
    rewritten_bullets: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    interview_questions: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )