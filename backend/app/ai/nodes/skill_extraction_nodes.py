from concurrent.futures import ThreadPoolExecutor
from app.ai.chains.skill_extraction import extract_job_skills, extract_resume_skills
from app.ai.state import JobAnalysisState

def extract_skills_node(state: JobAnalysisState) -> JobAnalysisState:
    """
    Extract resume and job skills.

    We keep resume + JD extraction inside one node for now so we can run both LLM calls concurrently and reduce latency.
    """

    resume_text = state["resume_text"]
    job_description = state["job_description"]

    with ThreadPoolExecutor(max_workers=2) as executor:
        resume_future = executor.submit(extract_resume_skills, resume_text)
        job_future = executor.submit(extract_job_skills, job_description)

        resume_extraction = resume_future.result()
        job_extraction = job_future.result()

    return {
        "resume_extraction": resume_extraction,
        "job_extraction": job_extraction,
    }