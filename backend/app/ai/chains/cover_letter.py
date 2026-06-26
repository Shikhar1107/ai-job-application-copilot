import json
import re
from typing import Type, TypeVar

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError

from app.ai.llm.provider import get_llm
from app.ai.prompts.cover_letter import COVER_LETTER_SYSTEM_PROMPT
from app.schemas.analysis import CoverLetterResult, ResumeBulletRewrite

T = TypeVar("T", bound=BaseModel)

def _extract_json_from_text(text: str) -> dict:
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON object found in LLM response: {text}")

    return json.loads(match.group(0))

def _invoke_json_chain(
        schema: Type[T],
        system_prompt: str,
        user_content: str,
)-> T:
    llm = get_llm()

    schema_json = json.dumps(schema.model_json_schema(), indent = 2)

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    system_prompt
                    + "\n\n"
                    + "You must return only valid JSON. Do not return markdown. "
                    + "Do not add explanations outside JSON. "
                    + "The JSON must follow this schema:\n"
                    + schema_json
                )
            ),
            HumanMessage(content=user_content)
        ]
    )

    raw_content = response.content

    if not isinstance(raw_content, str):
        raise ValueError(f"Unexpected LLM response content: {raw_content}")
    
    parsed_json = _extract_json_from_text(raw_content)

    try:
        return schema.model_validate(parsed_json)
    except ValidationError as exc:
        raise ValueError(
            f"LLM returned JSON but it did not match schema. JSON: {parsed_json}"
        ) from exc
    

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
- Return a JSON object with only one key: cover_letter.
"""

    return _invoke_json_chain(
        schema=CoverLetterResult,
        system_prompt=COVER_LETTER_SYSTEM_PROMPT,
        user_content=user_content,
    )