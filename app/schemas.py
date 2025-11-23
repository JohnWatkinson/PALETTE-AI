from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class QuestionnaireSubmission(BaseModel):
    """Schema for questionnaire submission"""
    # Personal information (GDPR required)
    first_name: str
    last_name: str
    email: EmailStr
    language: str = 'en'  # 'en' or 'it'

    # GDPR Consent
    privacy_consent: bool  # MANDATORY - must accept privacy policy
    newsletter_consent: bool = False  # OPTIONAL - Maison Guida marketing via Omnisend

    # Q1: Hair color
    hair_color: str

    # Q2: Skin tone
    skin_tone: str

    # Q3: Eye color
    eye_color: str

    # Q4: Vein color (strongest undertone indicator)
    vein_color: str

    # Q5: Jewelry preference
    jewelry_preference: str

    # Q6: Colors worn (multi-select)
    colors_worn: List[str]

    # Q7: Colors avoided (multi-select)
    colors_avoided: List[str]

    # Q8: Feedback
    color_feedback: str


class ColorInfo(BaseModel):
    """Individual color with name and hex code"""
    name: str
    hex: str


class PaletteResult(BaseModel):
    """Result returned after analysis"""
    season: str
    season_display_name: str
    confidence: int

    # Characteristics
    undertone: str
    value: str
    chroma: str

    # Colors
    core_neutrals: List[ColorInfo]
    accent_colors: List[ColorInfo]
    avoid_colors: List[str]

    # Optional explanation
    explanation: Optional[str] = None


class UserResponse(BaseModel):
    """User data for API responses"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
