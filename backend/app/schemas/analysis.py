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

class ResumeSkillExtraction(BaseModel):
    technical_skills: list[str] = Field(
        default_factory=list,
        description="Technical skills found in the resume.",
    )
    tools: list[str] = Field(
        default_factory=list,
        description="Tools, platforms, databases or libraries found in the resume.",
    )
    projects: list[str] = Field(
        default_factory=list,
        description="Relevant project or domain experience found in the resume.",
    )

class JobSkillExtraction(BaseModel):
    required_skills: list[str] = Field(
        default_factory=list,
        description="Required skills explicitly mentioned in the job description.",
    )
    preferred_skills: list[str] = Field(
        default_factory=list,
        description="Preferred or nice-to-have skills mentioned in the job description.",
    )
    tools: list[str] = Field(
        default_factory=list,
        description="Tools, frameworks, databases, or platforms mentioned in the job description."
    )
    responsibilities: list[str] = Field(
        default_factory=list,
        description="Main respondibiliteis from the job description.",
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