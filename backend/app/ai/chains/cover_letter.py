from app.ai.utils.json_parser import invoke_json_chain, invoke_text_chain
from app.ai.prompts.cover_letter import COVER_LETTER_SYSTEM_PROMPT
from app.schemas.analysis import CoverLetterResult, ResumeBulletRewrite

def generate_cover_letter(
        resume_text: str,
        job_description: str,
        fit_score: int,
        fit_summary: str,
        matched_skills: list[str],
        missing_skills: list[str],
        rewritten_bullets: list[ResumeBulletRewrite],
) -> CoverLetterResult:
    matched_skills_text = ", ".join(matched_skills) if matched_skills else "None"
    missing_skills_text = ", ".join(missing_skills) if missing_skills else "None"
    rewritten_bullets_text = "\n".join(
        f"- {item.rewritten_bullet}" for item in rewritten_bullets
    )

    user_content = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Fit Score:
{fit_score}

Fit Summary:
{fit_summary}

Matched Skills:
{matched_skills_text}

Missing Skills:
{missing_skills_text}

Rewritten Resume Bullets:
{rewritten_bullets_text}

Task:
Write a tailored cover letter for this job application.

Important:
- Highlight the strongest matched skills.
- Use the rewritten resume bullets as supporting evidence.
- Do not claim the candidate has missing skills unless they are clearly present in the resume.
- If missing skills are important, position them as areas of quick ramp-up or adjacent learning.
- Return only the final cover letter text.
- Do not return JSON.
- Do not return markdown.
"""

    cover_letter_text = invoke_text_chain(
    system_prompt=(
        COVER_LETTER_SYSTEM_PROMPT
        + "\n\nReturn only the cover letter text. "
        + "Do not return JSON. Do not use markdown. "
        + "Do not add explanations before or after the letter."
        ),
        user_content=user_content,
    )

    return CoverLetterResult(cover_letter=cover_letter_text)