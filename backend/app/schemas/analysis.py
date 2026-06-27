from pydantic import BaseModel, Field
from datetime import datetime
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

class RewriteBulletsRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)


class RewriteBulletsResponse(BaseModel):
    rewritten_bullets: list[ResumeBulletRewrite]

class InterviewQuestion(BaseModel):
    question: str = Field(
        ...,
        description="Interview question generated for the candidate.",
    )
    answer: str = Field(
        ...,
        description="Suggested answer or answer framework for the question.",
    )
    category: str = Field(
        ...,
        description="Question category such as RAG, FastAPI, LangChain, System Design, Behavioral.",
    )
    difficulty: str = Field(
        ...,
        description="Difficulty level: Easy, Medium, or Hard.",
    )
    evaluation_focus: str = Field(
        default="",
        description="What the interviewer is trying to evaluate with this question.",
    )

class InterviewQuestionsResult(BaseModel):
    interview_questions: list[InterviewQuestion] = Field(
        default_factory=list,
        description="Interview preparation questions generated for the target job.",
    )


class InterviewQuestionsRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)
    fit_score: int = Field(..., ge=0, le=100)
    fit_summary: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)


class InterviewQuestionsResponse(BaseModel):
    interview_questions: list[InterviewQuestion]

class CoverLetterResult(BaseModel):
    cover_letter: str = Field(
        ...,
        description="A tailored cover letter generated from the resume and job description.",
    )

class CoverLetterRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)
    fit_score: int = Field(..., ge=0, le=100)
    fit_summary: str
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    rewritten_bullets: list[ResumeBulletRewrite] = Field(default_factory=list)


class CoverLetterResponse(BaseModel):
    cover_letter: str

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


class AnalysisHistoryItem(BaseModel):
    id: int
    fit_score: int
    fit_summary: str
    matched_skills: list[str]
    missing_skills: list[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AnalysisDetailResponse(BaseModel):
    id: int
    resume_text: str
    job_description: str

    fit_score: int
    fit_summary: str

    resume_skills: list[str]
    job_required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]

    rewritten_bullets: list[ResumeBulletRewrite]
    cover_letter: str | None
    interview_questions: list[InterviewQuestion]

    created_at: datetime

    model_config = {
        "from_attributes": True
    }