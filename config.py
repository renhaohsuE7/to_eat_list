# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_maps_api_key: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()
