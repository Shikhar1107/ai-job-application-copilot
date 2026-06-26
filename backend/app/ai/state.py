from typing import TypedDict
from app.schemas.analysis import JobSkillExtraction, ResumeSkillExtraction

class JobAnalysisState(TypedDict, total=False):
    resume_text: str
    job_description: str
    resume_extraction: ResumeSkillExtraction
    job_extraction: JobSkillExtraction
    resume_skills: list[str]
    job_required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    fit_score: int
    fit_summary: str
    