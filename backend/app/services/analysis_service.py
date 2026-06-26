from app.ai.chains.cover_letter import generate_cover_letter
from app.ai.chains.interview_prep import generate_interview_questions
from app.ai.chains.resume_rewrite import rewrite_resume_bullets
from app.ai.graphs.job_analysis_graph import job_analysis_graph
from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
    RewriteBulletsRequest,
    RewriteBulletsResponse,
)


def analyze_application(payload: AnalyzeRequest) -> AnalyzeResponse:
    graph_result = job_analysis_graph.invoke(
        {
            "resume_text": payload.resume_text,
            "job_description": payload.job_description,
        }
    )
    print("GRAPH RESULT JOB SKILLS:", graph_result["job_required_skills"])
    print("TYPE OF FIRST JOB SKILL:", type(graph_result["job_required_skills"][0]))
    return AnalyzeResponse(
        fit_score=graph_result["fit_score"],
        fit_summary=graph_result["fit_summary"],
        resume_skills=graph_result["resume_skills"],
        job_required_skills=graph_result["job_required_skills"],
        matched_skills=graph_result["matched_skills"],
        missing_skills=graph_result["missing_skills"],
        rewritten_bullets=[],
        cover_letter="",
        interview_questions=[],
    )


def generate_resume_rewrites(
    payload: RewriteBulletsRequest,
) -> RewriteBulletsResponse:
    rewrite_result = rewrite_resume_bullets(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        matched_skills=payload.matched_skills,
        missing_skills=payload.missing_skills,
    )

    return RewriteBulletsResponse(
        rewritten_bullets=rewrite_result.rewritten_bullets,
    )


def generate_tailored_cover_letter(
    payload: CoverLetterRequest,
) -> CoverLetterResponse:
    cover_letter_result = generate_cover_letter(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        fit_score=payload.fit_score,
        fit_summary=payload.fit_summary,
        matched_skills=payload.matched_skills,
        missing_skills=payload.missing_skills,
        rewritten_bullets=payload.rewritten_bullets,
    )

    return CoverLetterResponse(
        cover_letter=cover_letter_result.cover_letter,
    )


def generate_tailored_interview_questions(
    payload: InterviewQuestionsRequest,
) -> InterviewQuestionsResponse:
    interview_result = generate_interview_questions(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        fit_score=payload.fit_score,
        fit_summary=payload.fit_summary,
        matched_skills=payload.matched_skills,
        missing_skills=payload.missing_skills,
    )

    return InterviewQuestionsResponse(
        interview_questions=interview_result.interview_questions,
    )