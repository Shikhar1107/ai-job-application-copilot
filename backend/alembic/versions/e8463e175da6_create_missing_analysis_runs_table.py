"""create missing analysis runs table

Revision ID: e8463e175da6
Revises: aea456276cbe
Create Date: 2026-07-08 16:37:26.774036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e8463e175da6'
down_revision: Union[str, Sequence[str], None] = 'aea456276cbe'
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
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    op.drop_table("analysis_runs")