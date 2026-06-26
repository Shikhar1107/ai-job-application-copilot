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

class SkillItem(BaseModel):
    name: str = Field(
        ...,
        description = "Skill name exactly as extracted from text"
    )
    canonical_name: str = Field(
        ...,
        description= "Standardized skill name used for matching"
    )
    category: str = Field(
        default="Other",
        description="Skill category such as Programming, Framework, Database, Cloud, AI/ML, Devops or Other."
    )
    evidence: str = Field(
        default="",
        description="Short phrase from the source text that supports this skill."
    )

class ResumeSkillExtraction(BaseModel):
    skills: list[SkillItem] = Field(
        default_factory=list,
        description="Skills and technical experience extracted from the resume.",
    )
    project_experience: list[str] = Field(
        default_factory=list,
        description="Relevant project or domain experience found in the resume.",
    )

class JobSkillExtraction(BaseModel):
    required_skills: list[SkillItem] = Field(
        default_factory=list,
        description="Required skills from the job description.",
    )
    preferred_skills: list[SkillItem] = Field(
        default_factory=list,
        description="Preferred or nice-to-have skills from the job description.",
    )
    responsibilities: list[str] = Field(
        default_factory=list,
        description="Main responsibilities from the job description.",
    )

class ResumeBulletRewrite(BaseModel):
    original_bullet: str
    rewritten_bullet: str
    reason: str

class ResumeRewriteResult(BaseModel):
    rewritten_bullets: list[ResumeBulletRewrite] = Field(
        default_factory=list,
        description="Resume bullets rewritten to better align with the job description."
    )

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