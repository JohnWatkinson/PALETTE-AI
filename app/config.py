from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str = "postgresql://palette:palette@localhost:5433/palette"

    # Email Service (Resend)
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "ciao@maisonguida.com"

    # Medusa API
    MEDUSA_API_URL: str = "http://localhost:9000"
    MEDUSA_PUBLISHABLE_KEY: Optional[str] = None

    # App Settings
    APP_PORT: int = 8001
    DEBUG: bool = True
    TESTING_MODE: bool = False  # Disable emails during testing

    # Optional: AI for photo analysis
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
