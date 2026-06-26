import json
import re
from typing import Type, TypeVar
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError
from app.ai.llm.provider import get_llm
from app.ai.prompts.resume_rewrite import RESUME_REWRITE_SYSTEM_PROMPT
from app.schemas.analysis import ResumeRewriteResult

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
) -> T:
    llm = get_llm()
    schema_json = json.dumps(schema.model_json_schema(), indent=2)

    response = llm.invoke(
        [
            SystemMessage(content=(
                system_prompt
                + "/n/n"
                + "You must return only valid JSON. Do not return markdown. "
                + "Do not add explanations outside JSON. " 
                + "The JSON must follow this schema:\n"
                + schema_json
            )
            ),
            HumanMessage(content=user_content),
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

    return _invoke_json_chain(
        schema=ResumeRewriteResult,
        system_prompt=RESUME_REWRITE_SYSTEM_PROMPT,
        user_content=user_content,
    )

