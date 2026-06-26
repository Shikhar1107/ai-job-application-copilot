from app.ai.utils.json_parser import invoke_json_chain
from app.ai.prompts.resume_rewrite import RESUME_REWRITE_SYSTEM_PROMPT
from app.schemas.analysis import ResumeRewriteResult

def rewrite_resume_bullets(
    resume_text: str,
    job_description: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> ResumeRewriteResult:
    matched_skills_text = ", ".join(matched_skills) if matched_skills else "None"
    missing_skills_text = ", ".join(missing_skills) if missing_skills else "None"

    user_content = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Matched Skills:
{matched_skills_text}

Missing Skills:
{missing_skills_text}

Task:
Rewrite 3 to 5 resume bullets from the resume to better align with the job description.

Important:
- Use matched skills where relevant.
- Do not add missing skills unless they are explicitly present in the resume.
- If the resume is not written as bullet points, convert the strongest resume statements into resume-style bullets.
- For each item, return:
  - original_bullet
  - rewritten_bullet
  - reason
"""

    return invoke_json_chain(
        schema=ResumeRewriteResult,
        system_prompt=RESUME_REWRITE_SYSTEM_PROMPT,
        user_content=user_content,
    )

