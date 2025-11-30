import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Career Coach"
    OLLAMA_MODEL: str = "gpt-oss:120b-cloud"
    PROMPT_TEMPLATE_PATH: str = "resources/prompt.txt"
    LOG_LEVEL: str = "TRACE"

    class Config:
        env_file = ".env"

settings = Settings()
