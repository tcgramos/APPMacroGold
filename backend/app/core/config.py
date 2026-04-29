from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "APPMacroGold"
    api_prefix: str = "/api/v1"
    postgres_url: str = "sqlite:///./app.db"
    redis_url: str = "redis://localhost:6379/0"
    rabbit_url: str = "amqp://guest:guest@localhost:5672/"
    secret_key: str = "dev-secret"

    score_weight_dxy: int = 20
    score_weight_us10y: int = 20
    score_weight_silver: int = 15
    score_weight_copper: int = 10
    score_weight_platinum: int = 10
    score_weight_commodities: int = 10
    score_weight_fed: int = 15

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
