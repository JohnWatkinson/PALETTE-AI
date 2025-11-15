from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User table - stores email and consent"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    newsletter_consent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    responses = relationship("Response", back_populates="user", cascade="all, delete-orphan")
    palettes = relationship("Palette", back_populates="user", cascade="all, delete-orphan")


class Response(Base):
    """Questionnaire responses table"""
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Physical characteristics
    hair_color = Column(String(50))
    skin_tone = Column(String(50))
    eye_color = Column(String(50))
    vein_color = Column(String(50))
    jewelry_preference = Column(String(50))

    # Color preferences (JSON arrays)
    colors_worn = Column(JSON)  # List of color categories they wear
    colors_avoided = Column(JSON)  # List of color categories they avoid

    # Feedback question
    color_feedback = Column(String(50))  # How people say they look in colors

    # Metadata
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="responses")


class Palette(Base):
    """Generated color palette results"""
    __tablename__ = "palettes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Season determination
    season = Column(String(50), nullable=False)  # e.g., "bright_spring"
    season_display_name = Column(String(100))  # e.g., "Bright Spring"
    confidence = Column(Integer)  # 0-100

    # Characteristics determined
    undertone = Column(String(20))  # warm/cool/neutral
    value = Column(String(20))  # light/medium/deep
    chroma = Column(String(20))  # bright/muted/soft/rich
    contrast = Column(String(20))  # high/medium/low

    # Color palette (JSON with hex codes)
    core_neutrals = Column(JSON)  # [{"name": "Camel", "hex": "#C19A6B"}, ...]
    accent_colors = Column(JSON)  # [{"name": "Coral", "hex": "#FF6F61"}, ...]
    avoid_colors = Column(JSON)  # ["Black", "Navy", ...]

    # Optional: AI-generated explanation
    explanation = Column(Text, nullable=True)

    # Metadata
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="palettes")


class PhotoAnalysis(Base):
    """Photo analysis results (Phase 5 - optional)"""
    __tablename__ = "photo_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    photo_path = Column(String(500))
    refined_season = Column(String(50))
    ai_analysis = Column(JSON)  # Full AI response
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
