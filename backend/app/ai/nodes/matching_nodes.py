from app.ai.state import JobAnalysisState
from app.services.skill_matching_service import (
    dedupe_skill_items,
    match_skills,
    skill_names,
)


def match_skills_node(state: JobAnalysisState) -> JobAnalysisState:
    resume_extraction = state["resume_extraction"]
    job_extraction = state["job_extraction"]

    resume_skill_items = dedupe_skill_items(resume_extraction.skills)
    job_required_skill_items = dedupe_skill_items(job_extraction.required_skills)

    resume_skill_names = skill_names(resume_skill_items)
    job_required_skill_names = skill_names(job_required_skill_items)

    matched_skills, missing_skills = match_skills(
        resume_skills=resume_skill_items,
        job_skills=job_required_skill_items,
    )

    return {
        "resume_skills": resume_skill_names,
        "job_required_skills": job_required_skill_names,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }