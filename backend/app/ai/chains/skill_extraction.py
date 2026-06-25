import json
import re
from typing import Type, TypeVar

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError

from app.ai.llm.provider import get_llm
from app.ai.prompts.skill_extraction import (
    JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
    RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
)
from app.schemas.analysis import JobSkillExtraction, ResumeSkillExtraction

T = TypeVar("T", bound=BaseModel)

def _extract_json_from_text(text:str)-> dict:
    """
    Extract JSON object from an LLM response.

    Handles cases where the model returns:
    - pure JSON
    - markdown fenced JSON
    - extra text around JSON
    """
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?","",text)
        text = re.sub(r"```$","",text)
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}",text,re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response: {text}")
    
    return json.loads(match.group(0))

def _invoke_json_extraction(
    schema: Type[T],
    system_prompt: str,
    user_content: str,
) -> T:
    llm = get_llm()

    schema_json = json.dumps(schema.model_json_schema(), indent=2)

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    system_prompt
                    + "\n\n"
                    + "You must return only valid JSON. Do not return markdown. "
                    + "Do not add explanations. The JSON must follow this schema:\n"
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

def extract_resume_skills(resume_text: str) -> ResumeSkillExtraction:
    return _invoke_json_extraction(
        schema=ResumeSkillExtraction,
        system_prompt=RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
        user_content=f"Resume:\n\n{resume_text}",
    )


def extract_job_skills(job_description: str) -> JobSkillExtraction:
    return _invoke_json_extraction(
        schema=JobSkillExtraction,
        system_prompt=JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
        user_content=f"Job Description:\n\n{job_description}",
    )