from fastapi import APIRouter

from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    InterviewQuestion,
    ResumeBulletRewrite,
)

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_job_application(payload: AnalyzeRequest) -> AnalyzeResponse:
    """
    Mock job application analysis endpoint.

    This endpoint confirms the API contract before we connect the real LangGraph workflow.
    """

    return AnalyzeResponse(
        fit_score=82,
        fit_summary=(
            "The candidate is a strong match for the role based on Python, "
            "FastAPI, LangChain, and GenAI project experience. The main gaps "
            "are deeper PostgreSQL production experience and formal LangGraph "
            "workflow deployment experience."
        ),
        resume_skills=[
            "Python",
            "FastAPI",
            "LangChain",
            "RAG",
            "Docker",
            "MLflow"
        ],
        job_required_skills=[
            "Python",
            "FastAPI",
            "LangChain",
            "LangGraph",
            "PostgreSQL",
            "Docker",
        ],
        matched_skills=[
            "Python",
            "FastAPI",
            "LangChain",
            "Docker",
        ],
        missing_skills=[
            "PostgreSQL",
            "LangGraph",
        ],
        rewritten_bullets=[
            ResumeBulletRewrite(
                original_bullet=(
                    "Built RAG pipeline using LangChain for document question answering."
                ),
                rewritten_bullet=(
                    "Developed a production-style RAG pipeline using LangChain, "
                    "FastAPI, vector search, and Docker to deliver context-aware "
                    "answers over domain-specific documents."
                ),
                reason=(
                    "The rewritten bullet adds backend, deployment, and production "
                    "keywords that align better with GenAI Engineer roles."
                ),
            )
        ],
        cover_letter=(
            "Dear Hiring Manager,\n\n"
            "I am excited to apply for this role because my experience with Python, "
            "FastAPI, LangChain, RAG systems, Docker, and LLM-based applications "
            "aligns closely with your requirements. I have built hands-on GenAI "
            "projects involving retrieval pipelines, API development, and deployment-focused "
            "engineering practices.\n\n"
            "Best regards,\n"
            "Candidate"
        ),
        interview_questions=[
            InterviewQuestion(
                question="How would you design a LangGraph workflow for a multi-step job analysis pipeline?",
                category="LangGraph",
                difficulty="Medium",
            ),
            InterviewQuestion(
                question="How do you evaluate whether a RAG system is returning grounded answers?",
                category="RAG",
                difficulty="Medium",
            ),
            InterviewQuestion(
                question="How would you deploy a FastAPI-based LLM application on Render?",
                category="Deployment",
                difficulty="Easy",
            ),
        ],
    )