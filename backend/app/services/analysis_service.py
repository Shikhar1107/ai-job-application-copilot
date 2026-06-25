from app.ai.chains.skill_extraction import extract_job_skills, extract_resume_skills
from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    InterviewQuestion,
    ResumeBulletRewrite,
)

def _normalize_skills(skill: str)-> str:
    return skill.strip().lower()

def _match_skills(resume_skills: list[str], job_skills: list[str])  -> tuple[list[str],list[str]]:
    resume_skill_map = {_normalize_skills(skill): skill for skill in resume_skills}
    job_skill_map = {_normalize_skills(skill): skill for skill in job_skills}
    matched = []
    missing = []

    for normalized_job_skill, original_job_skill in job_skill_map.items():
        if normalized_job_skill in resume_skill_map:
            matched.append(original_job_skill)
        else:
            missing.append(original_job_skill)
    
    return matched, missing

def analyze_application(payload: AnalyzeRequest) -> AnalyzeResponse:
    resume_extraction = extract_resume_skills(payload.resume_text)
    job_extraction = extract_job_skills(payload.job_description)

    resume_skills = sorted(
        set(
            resume_extraction.technical_skills + resume_extraction.tools + resume_extraction.projects
        )
    )

    job_required_skills = sorted(
        set(
            job_extraction.required_skills
            + job_extraction.tools,
        )
    )

    matched_skills, missing_skills = _match_skills(
        resume_skills=resume_skills, job_skills=job_required_skills
    )

    return AnalyzeResponse(
        fit_score=82,
        fit_summary=(
            "This is still a temporary mock summary. Real fit scoring will be added "
            "in the next backend phase. Skill extraction is now powered by the LLM."
        ),
        resume_skills=resume_skills,
        job_required_skills=job_required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        rewritten_bullets=[
            ResumeBulletRewrite(
                original_bullet="Built RAG pipeline using LangChain.",
                rewritten_bullet=(
                    "Built a production-style RAG pipeline using LangChain, FastAPI, "
                    "and vector search to deliver context-aware AI responses."
                ),
                reason="Temporary mock bullet rewrite. Real rewriting will be added later.",
            )
        ],
        cover_letter=(
            "Temporary mock cover letter. Real cover letter generation will be added later."
        ),
        interview_questions=[
            InterviewQuestion(
                question="Temporary mock question. Real interview generation will be added later.",
                category="General",
                difficulty="Easy",
            )
        ],
    )