import time
from app.ai.chains.skill_extraction import extract_job_skills, extract_resume_skills
from app.schemas.analysis import (
    AnalyzeRequest,
    AnalyzeResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
    RewriteBulletsRequest,
    RewriteBulletsResponse,
    SkillItem,
)
from app.services.scoring_service import calculate_fit_score
from app.ai.chains.resume_rewrite import rewrite_resume_bullets
from app.ai.chains.cover_letter import generate_cover_letter
from app.ai.chains.interview_prep import generate_interview_questions 
from concurrent.futures import ThreadPoolExecutor

def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _dedupe_strings(items: list[str]) -> list[str]:
    cleaned = []

    for item in items:
        value = item.strip()
        if value:
            cleaned.append(value)

    return sorted(set(cleaned), key=str.lower)


def _dedupe_skill_items(skills: list[SkillItem]) -> list[SkillItem]:
    skill_map = {}

    for skill in skills:
        key = _normalize_text(skill.canonical_name)
        if key and key not in skill_map:
            skill_map[key] = skill

    return list(skill_map.values())


def _skill_names(skills: list[SkillItem]) -> list[str]:
    return _dedupe_strings([skill.canonical_name for skill in skills])


def _match_skills(
    resume_skills: list[SkillItem],
    job_skills: list[SkillItem],
) -> tuple[list[str], list[str]]:
    resume_canonical_names = {
        _normalize_text(skill.canonical_name)
        for skill in resume_skills
    }

    matched = []
    missing = []

    for job_skill in job_skills:
        normalized_job_skill = _normalize_text(job_skill.canonical_name)

        if normalized_job_skill in resume_canonical_names:
            matched.append(job_skill.canonical_name)
        else:
            missing.append(job_skill.canonical_name)

    return _dedupe_strings(matched), _dedupe_strings(missing)


def analyze_application(payload: AnalyzeRequest) -> AnalyzeResponse:

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        resume_future = executor.submit(extract_resume_skills, payload.resume_text)
        job_future = executor.submit(extract_job_skills, payload.job_description)

        resume_extraction = resume_future.result()
        job_extraction = job_future.result()

    print(f"Skill extraction completed in {time.perf_counter() - start_time:.2f}s")
    resume_skill_items = _dedupe_skill_items(resume_extraction.skills)
    job_required_skill_items = _dedupe_skill_items(job_extraction.required_skills)

    resume_skills = _skill_names(resume_skill_items)
    job_required_skills = _skill_names(job_required_skill_items)

    matched_skills, missing_skills = _match_skills(
        resume_skills=resume_skill_items,
        job_skills=job_required_skill_items,
    )

    fit_score_result = calculate_fit_score(
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        required_skills=job_required_skills,
        resume_skills=resume_skills,
    )

    # resume_rewrite_result = rewrite_resume_bullets(
    #     resume_text=payload.resume_text,
    #     job_description=payload.job_description,
    #     matched_skills=matched_skills,
    #     missing_skills=missing_skills,
    # )

    # cover_letter_result = generate_cover_letter(
    #     resume_text=payload.resume_text,
    #     job_description=payload.job_description,
    #     fit_score=fit_score_result.score,
    #     fit_summary=fit_score_result.summary,
    #     matched_skills=matched_skills,
    #     missing_skills=missing_skills,
    #     rewritten_bullets=resume_rewrite_result.rewritten_bullets
    #     )

    return AnalyzeResponse(
        fit_score=fit_score_result.score,
        fit_summary=fit_score_result.summary,
        resume_skills=resume_skills,
        job_required_skills=job_required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        rewritten_bullets=[],
        cover_letter="",
        interview_questions=[],
    )


def generate_resume_rewrites(
        payload: RewriteBulletsRequest,
)-> RewriteBulletsResponse:
    rewrite_result = rewrite_resume_bullets(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        matched_skills=payload.matched_skills,
        missing_skills=payload.missing_skills,
    )

    return RewriteBulletsResponse(
        rewritten_bullets = rewrite_result.rewritten_bullets
    )

def generate_tailored_cover_letter(
        payload: CoverLetterRequest
) -> CoverLetterResponse:
    cover_letter_result = generate_cover_letter(
        resume_text=payload.resume_text,
        job_description= payload.job_description,
        fit_score=payload.fit_score,
        fit_summary=payload.fit_summary,
        matched_skills=payload.matched_skills,
        missing_skills= payload.missing_skills,
        rewritten_bullets=payload.rewritten_bullets,
    )

    return CoverLetterResponse(
        cover_letter= cover_letter_result.cover_letter,
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