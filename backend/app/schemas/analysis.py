from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(
        ...,
        min_length=50,
        description="Candidate resume text pasted by the user"
    )
    job_description: str = Field(
        ...,
        min_length=50,
        description="Job description text pasted by the user.",
    )

class ResumeBulletRewrite(BaseModel):
    original_bullet: str
    rewritten_bullet: str
    reason: str

class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str

class AnalyzeResponse(BaseModel):
    fit_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Resume-job fit score from 0 to 100.",
    )
    fit_summary: str
    resume_skills: list[str]
    job_required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]

    rewritten_bullets: list[ResumeBulletRewrite]
    cover_letter: str
    interview_questions: list[InterviewQuestion]