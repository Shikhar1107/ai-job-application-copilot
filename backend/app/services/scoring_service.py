from dataclasses import dataclass

@dataclass
class FitScoreResult:
    score: int
    summary: str

def _normalize_skill(skill: str) -> str:
    return skill.strip().lower()

def _calculate_match_percentage(
        matched_skills: list[str],
        required_skills: list[str],
) -> float:
    if not required_skills:
        return 0.0
    
    return len(matched_skills) / len(required_skills)

def calculate_fit_score(
        matched_skills: list[str],
        missing_skills: list[str],
        required_skills: list[str],
        resume_skills: list[str],
) -> FitScoreResult:
    """
    Calculate a deterministic resume-job fit score.
    
        Scoring logic:
        - 80 points: required skill coverage
        - 10 points: breadth of resume skills
        - 10 points: low missing-skill penalty / completeness bonus
    
        This is intentionally deterministic so the score is stable and explainable.
    """

    required_match_ratio = _calculate_match_percentage(
        matched_skills=matched_skills,
        required_skills=required_skills,
    )

    required_skill_score = required_match_ratio * 80

    # Breadth bonus: reward resumes that show a reasonable technical range.
    # Cap at 10 points.
    breadth_bonus = min(len(resume_skills) * 0.75, 10)

    # Completeness bonus: reward fewer missing required skills.
    if required_skills:
        missing_ratio = len(missing_skills) / len(required_skills)
        completeness_bonus = max(0, 10 - (missing_ratio * 10))
    else:
        completeness_bonus = 0

    raw_score = required_skill_score + breadth_bonus + completeness_bonus
    final_score = max(0, min(100, round(raw_score)))

    summary = _build_fit_summary(
        score=final_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        required_skills=required_skills,
    )

    return FitScoreResult(score=final_score, summary=summary)

def _build_fit_summary(
    score: int,
    matched_skills: list[str],
    missing_skills: list[str],
    required_skills: list[str],
) -> str:
    total_required = len(required_skills)
    total_matched = len(matched_skills)

    if total_required == 0:
        return (
            "The job description did not contain enough clearly extractable required skills, "
            "so the fit score is based on limited information."
        )

    if score >= 85:
        fit_level = "strong"
    elif score >= 70:
        fit_level = "good"
    elif score >= 50:
        fit_level = "moderate"
    else:
        fit_level = "weak"

    matched_text = ", ".join(matched_skills[:6]) if matched_skills else "none"
    missing_text = ", ".join(missing_skills[:6]) if missing_skills else "none"

    return (
        f"The candidate appears to be a {fit_level} match for this role. "
        f"They match {total_matched} out of {total_required} required skills. "
        f"Matched skills include: {matched_text}. "
        f"Missing or less visible skills include: {missing_text}."
    )