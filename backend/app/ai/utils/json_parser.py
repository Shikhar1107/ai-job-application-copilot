import json
import re
from typing import Type, TypeVar

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, ValidationError

from app.ai.llm.provider import get_llm

T = TypeVar("T", bound=BaseModel)


def extract_json_from_text(text: str) -> dict:
    """
    Extract a JSON object from an LLM response.

    Supports:
    - pure JSON
    - markdown fenced JSON
    - extra explanatory text around JSON
    """

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


def invoke_json_chain(
    schema: Type[T],
    system_prompt: str,
    user_content: str,
) -> T:
    """
    Invokes the configured LLM and validates the response against a Pydantic schema.

    This avoids depending on model-native structured output, which may not work
    reliably across all OpenRouter/free models.
    """

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

    print("\n========== LLM DEBUG START ==========")
    print("Response type:", type(response))
    print("Response:", response)
    print("Response content repr:", repr(raw_content))
    print("Response additional_kwargs:", getattr(response, "additional_kwargs", None))
    print("Response response_metadata:", getattr(response, "response_metadata", None))
    print("========== LLM DEBUG END ==========\n")

    if not isinstance(raw_content, str):
        raise ValueError(f"Unexpected LLM response content: {raw_content}")

    if not raw_content.strip():
        raise ValueError(
            "LLM returned empty content. "
            f"Full response metadata: {getattr(response, 'response_metadata', None)}"
        )

    parsed_json = extract_json_from_text(raw_content)

    try:
        return schema.model_validate(parsed_json)
    except ValidationError as exc:
        raise ValueError(
            f"LLM returned JSON but it did not match schema. JSON: {parsed_json}"
        ) from exc
    
def invoke_text_chain(
    system_prompt: str,
    user_content: str,
) -> str:
    """
    Invokes the configured LLM and returns plain text.

    Used for outputs where JSON mode is unstable with certain free/reasoning models.
    """

    llm = get_llm()

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content),
        ]
    )

    raw_content = response.content

    print("\n========== TEXT LLM DEBUG START ==========")
    print("Response:", response)
    print("Content repr:", repr(raw_content))
    print("Metadata:", getattr(response, "response_metadata", None))
    print("========== TEXT LLM DEBUG END ==========\n")

    if not isinstance(raw_content, str):
        raise ValueError(f"Unexpected LLM response content: {raw_content}")

    if not raw_content.strip():
        raise ValueError(
            "LLM returned empty plain-text content. "
            f"Full response metadata: {getattr(response, 'response_metadata', None)}"
        )

    return raw_content.strip()