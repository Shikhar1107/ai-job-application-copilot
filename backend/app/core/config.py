from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "ResumeIQ — Agentic Resume Analysis System"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "*"
    OPENROUTER_API_KEY: str=""
    OPENROUTER_BASE_URL: str = "http://openrouter.ai/api/v1"
    LLM_MODEL: str = "openai/gpt-oss-120b:free"
    LLM_TEMPERATURE: float = 0.2
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_job_copilot"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive= True,
    )

settings = Settings()