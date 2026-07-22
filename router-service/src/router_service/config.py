from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"
    notification_service_url: str = "http://localhost:8001/internal/v1/emails"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
