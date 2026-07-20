from app.ai.utils.json_parser import invoke_json_chain
from app.ai.prompts.skill_extraction import (
    JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
    RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
)
from app.schemas.analysis import JobSkillExtraction, ResumeSkillExtraction
import re
from app.schemas.analysis import SkillItem

COMMON_SKILLS = [
    "Python",
    "Java",
    "FastAPI",
    "Flask",
    "Django",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "RAG",
    "Retrieval-Augmented Generation",
    "OpenAI",
    "Anthropic",
    "Gemini",
    "Llama",
    "Hugging Face",
    "Transformers",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Chroma",
    "Milvus",
    "Pinecone",
    "FAISS",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "CI/CD",
    "MLflow",
    "Streamlit",
    "React",
    "TypeScript",
    "REST API",
    "Microservices",
    "Prompt Engineering",
    "Vector Database",
    "MCP",
    "AI Agent",
]


def fallback_extract_skills(text: str) -> list[SkillItem]:
    found = []

    for skill in COMMON_SKILLS:
        pattern = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
        match = pattern.search(text)

        if match:
            found.append(
                SkillItem(
                    name=skill,
                    canonical_name=skill,
                    category="Other",
                    evidence=text[max(0, match.start() - 40): match.end() + 40],
                )
            )

    # Remove duplicates by canonical name
    unique = {}
    for skill in found:
        unique[skill.canonical_name.lower()] = skill

    return list(unique.values())

def extract_resume_skills(resume_text: str) -> ResumeSkillExtraction:
    return invoke_json_chain(
        schema=ResumeSkillExtraction,
        system_prompt=RESUME_SKILL_EXTRACTION_SYSTEM_PROMPT,
        user_content=f"Resume:\n\n{resume_text}",
    )


def extract_job_skills(job_description: str) -> JobSkillExtraction:

    try:
        return invoke_json_chain(
            schema=JobSkillExtraction,
            system_prompt=JOB_SKILL_EXTRACTION_SYSTEM_PROMPT,
            user_content=f"Job Description:\n\n{job_description}",
        )
    except Exception as e:
        print(f"Job skill extraction failed, using fallback. Error: {e}")

        return JobSkillExtraction(
            required_skills=fallback_extract_skills(job_description),
            preferred_skills=[],
            responsibilities=[],
        )