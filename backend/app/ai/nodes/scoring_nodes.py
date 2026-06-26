from app.ai.state import JobAnalysisState
from app.services.scoring_service import calculate_fit_score

def score_fit_node( state: JobAnalysisState) -> JobAnalysisState:
    fit_score_result = calculate_fit_score(
        matched_skills= state["matched_skills"],
        missing_skills= state["missing_skills"],
        required_skills= state["job_required_skills"],
        resume_skills= state["resume_skills"],
    )

    return {
        "fit_score": fit_score_result.score,
        "fit_summary": fit_score_result.summary,
    }