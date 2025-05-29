from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Healthcare Document Analysis"
    
    # File Upload Settings
    UPLOAD_DIR: str = "data/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Together API Settings
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
    
    # Model Settings
    TOGETHER_MODEL_NAME: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
    MODEL_TEMPERATURE: float = 0.7
    MODEL_MAX_TOKENS: int = 1000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings() 