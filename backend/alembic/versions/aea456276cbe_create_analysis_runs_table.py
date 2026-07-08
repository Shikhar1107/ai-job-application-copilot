"""create analysis runs table

Revision ID: aea456276cbe
Revises:
Create Date: 2026-07-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "aea456276cbe"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("resume_text", sa.Text(), nullable=False),
        sa.Column("job_description", sa.Text(), nullable=False),
        sa.Column("fit_score", sa.Integer(), nullable=False),
        sa.Column("fit_summary", sa.Text(), nullable=False),
        sa.Column("resume_skills", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("job_required_skills", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("matched_skills", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("missing_skills", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("cover_letter", sa.Text(), nullable=False, server_default=""),
        sa.Column("rewritten_bullets", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("interview_questions", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_index(
        "ix_analysis_runs_id",
        "analysis_runs",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_analysis_runs_id", table_name="analysis_runs")
    op.drop_table("analysis_runs")