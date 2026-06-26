import json 
import re
from typing import Type, TypeVar

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError

from app.ai.llm.provider import get_llm
from app.ai.prompts.interview_prep import INTERVIEW_PREP_SYSTEM_PROMPT
from app.schemas.analysis import InterviewQuestionsResult

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

def generate_interview_questions(
        resume_text: str,
        job_description: str,
        fit_score: int,
        fit_summary: str,
        matched_skills: list[str],
        missing_skills: list[str],
) -> InterviewQuestionsResult:
    matched_skills_text = ", ".join(matched_skills) if matched_skills else None
    missing_skills_text = ", ".join(missing_skills) if missing_skills else None

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

Task:
Generate 8 to 12 interview preparation questions with strong suggested answers for this candidate and job.

Question mix:
- 3 to 4 questions based on matched skills
- 2 to 3 project-deep-dive questions based on resume experience
- 2 questions based on missing or weaker skills
- 1 to 2 behavioral or communication questions

For each interview question, return:
- question
- answer
- category
- difficulty
- evaluation_focus

Answer rules:
- Answers should be practical and interview-ready.
- Answers should be written from the candidate's perspective using "I" where appropriate.
- Do not falsely claim experience with missing skills.
- For missing skills, answer using adjacent experience and a clear learning/design approach.
- Keep each answer around 80 to 160 words.
- Return a JSON object with the key interview_questions.

Important:
- Do not assume the candidate has experience with missing skills.
- For missing skills, frame questions as conceptual or learning-gap questions.
- Return a JSON object with the key interview_questions.
"""

    return _invoke_json_chain(
        schema=InterviewQuestionsResult,
        system_prompt=INTERVIEW_PREP_SYSTEM_PROMPT,
        user_content=user_content,
    )