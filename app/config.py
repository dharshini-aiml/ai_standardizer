"""Application configuration."""
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class Settings:
    """Application settings from environment variables."""
    
    # API Configuration
    API_TITLE: str = "Data Standardization API"
    API_VERSION: str = "1.0.0"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Gemini Configuration (ONLY)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Processing Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "30"))
    
    # Data Standardization
    QUALITY_SCORE_THRESHOLD: float = float(os.getenv("QUALITY_SCORE_THRESHOLD", "0.7"))
    
    # Logging
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_FILE: str = os.path.join(LOG_DIR, "app.log")
    
    @classmethod
    def get_config(cls) -> dict:
        """Return configuration as dictionary."""
        return {
            "api_title": cls.API_TITLE,
            "api_version": cls.API_VERSION,
            "log_level": cls.LOG_LEVEL,
            "gemini_enabled": bool(cls.GEMINI_API_KEY),
            "gemini_model": cls.GEMINI_MODEL,
            "max_retries": cls.MAX_RETRIES,
            "timeout_seconds": cls.TIMEOUT_SECONDS,
        }


settings = Settings()