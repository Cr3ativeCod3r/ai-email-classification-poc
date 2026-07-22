from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    smtp_host: str = "mailhog"
    smtp_port: int = 1025

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
