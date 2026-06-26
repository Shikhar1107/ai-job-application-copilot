from app.ai.utils.json_parser import invoke_json_chain
from app.ai.prompts.skill_extraction import (
    JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
    RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
)
from app.schemas.analysis import JobSkillExtraction, ResumeSkillExtraction


def extract_resume_skills(resume_text: str) -> ResumeSkillExtraction:
    return invoke_json_chain(
        schema=ResumeSkillExtraction,
        system_prompt=RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
        user_content=f"Resume:\n\n{resume_text}",
    )


def extract_job_skills(job_description: str) -> JobSkillExtraction:
    return invoke_json_chain(
        schema=JobSkillExtraction,
        system_prompt=JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
        user_content=f"Job Description:\n\n{job_description}",
    )