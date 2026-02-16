from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str
    api_key: str = "dev-key"
    storage_dir: str = "./storage"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
