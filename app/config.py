import os
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str
    weather_api_key: str = ""
    
    # Database
    database_url: str = "sqlite:///./farmer_db.db"
    
    # Server
    host: str = "localhost"
    port: int = 8000
    debug: bool = True
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()