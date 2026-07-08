from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Job Application Copilot"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    BACKEND_CORS_ORIGINS: str = "*"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_MODEL: str = "openai/gpt-oss-20b:free"
    LLM_TEMPERATURE: float = 0.2

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/ai_job_copilot"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        value = self.BACKEND_CORS_ORIGINS.strip()

        if value == "*":
            return ["*"]

        return [
            origin.strip().rstrip("/")
            for origin in value.split(",")
            if origin.strip()
        ]


settings = Settings()