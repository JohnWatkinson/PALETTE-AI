from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

from .config import settings
from .database import get_db, init_db
from .schemas import QuestionnaireSubmission, PaletteResult
from .models import User, Response, Palette
from .questionnaire import analyzer
from .email_service import email_service

# Create FastAPI app
app = FastAPI(
    title="PALETTE-AI",
    description="Color palette recommendation tool for Maison Guida",
    version="1.0.0",
    debug=settings.DEBUG
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🎨 PALETTE-AI is running!")
    print(f"📍 http://localhost:{settings.APP_PORT}")
    print(f"📚 API Docs: http://localhost:{settings.APP_PORT}/docs")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render questionnaire page"""
    return templates.TemplateResponse("questionnaire.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": "PALETTE-AI"}


@app.post("/api/submit", response_model=PaletteResult)
async def submit_questionnaire(
    submission: QuestionnaireSubmission,
    db: Session = Depends(get_db)
):
    """
    Process questionnaire submission:
    1. Analyze responses to determine season
    2. Save user, responses, and palette to database
    3. Return palette result
    """

    # Step 1: Analyze responses
    palette_result = analyzer.analyze(submission)

    # Step 2: Save to database
    try:
        # Create or get user
        user = db.query(User).filter(User.email == submission.email).first()
        if not user:
            # New user - create with GDPR fields
            user = User(
                first_name=submission.first_name,
                last_name=submission.last_name,
                email=submission.email,
                language=submission.language,
                privacy_consent=submission.privacy_consent,
                newsletter_consent=submission.newsletter_consent,
                submission_count=1,
                last_submission_at=func.now()
            )
            db.add(user)
            db.flush()  # Get user ID
        else:
            # Existing user - update consent and submission tracking
            user.privacy_consent = submission.privacy_consent
            user.newsletter_consent = submission.newsletter_consent
            user.submission_count += 1
            user.last_submission_at = func.now()

        # Save questionnaire response
        response = Response(
            user_id=user.id,
            hair_color=submission.hair_color,
            skin_tone=submission.skin_tone,
            eye_color=submission.eye_color,
            vein_color=submission.vein_color,
            jewelry_preference=submission.jewelry_preference,
            colors_worn=submission.colors_worn,
            colors_avoided=submission.colors_avoided,
            color_feedback=submission.color_feedback
        )
        db.add(response)

        # Save palette
        palette = Palette(
            user_id=user.id,
            season=palette_result.season,
            season_display_name=palette_result.season_display_name,
            confidence=palette_result.confidence,
            undertone=palette_result.undertone,
            value=palette_result.value,
            chroma=palette_result.chroma,
            core_neutrals=[color.dict() for color in palette_result.core_neutrals],
            accent_colors=[color.dict() for color in palette_result.accent_colors],
            avoid_colors=palette_result.avoid_colors,
            explanation=palette_result.explanation
        )
        db.add(palette)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save results")

    # Step 3: Send email with palette results
    email_sent = email_service.send_palette_email(submission.email, palette_result)
    if email_sent:
        print(f"✅ Palette email sent to {submission.email}")
    else:
        print(f"⚠️  Email not sent to {submission.email}")

    # Step 4: Return result
    return palette_result


@app.get("/api/palette/{email}")
async def get_user_palette(email: str, db: Session = Depends(get_db)):
    """Get latest palette for a user by email"""

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    palette = db.query(Palette).filter(Palette.user_id == user.id).order_by(Palette.generated_at.desc()).first()
    if not palette:
        raise HTTPException(status_code=404, detail="No palette found for this user")

    return {
        "season": palette.season,
        "season_display_name": palette.season_display_name,
        "confidence": palette.confidence,
        "undertone": palette.undertone,
        "value": palette.value,
        "chroma": palette.chroma,
        "core_neutrals": palette.core_neutrals,
        "accent_colors": palette.accent_colors,
        "avoid_colors": palette.avoid_colors,
        "generated_at": palette.generated_at
    }


@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    """Thank you page after submission"""
    return templates.TemplateResponse("thank-you.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
