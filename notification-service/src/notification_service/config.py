from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    smtp_host: str = "mailhog"
    smtp_port: int = 1025

    class Config:
        env_file = ".env"

settings = Settings()
