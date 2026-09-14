from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FootPredict API"
    API_V1_STR: str = "/api/v1"
    API_FOOTBALL_KEY: str
    API_FOOTBALL_BASE_URL: str = "https://v3.football.api-sports.io"
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()
