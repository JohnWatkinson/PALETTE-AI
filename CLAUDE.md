# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PALETTE-AI** is a color palette recommendation tool for Maison Guida (MG), a fashion brand. The app:
- Captures email addresses through an interactive color analysis questionnaire
- Determines the user's color "season" (Spring/Summer/Autumn/Winter) based on their responses
- Sends personalized color palette recommendations via email
- Recommends MG products that match the user's color profile
- Optional: Advanced photo analysis for deeper personalization

## Architecture

### Tech Stack
- **Backend:** FastAPI (Python), Uvicorn ASGI server
- **Database:** PostgreSQL (not SQLite - align with Medusa/ERPNext stack)
- **Frontend:** HTML/CSS/JavaScript (no framework), optional htmx for smooth interactions
- **Email Service:** Resend (via `ciao@maisonguida.com`)
- **Deployment:** VPS at subdomain `palette.maisonguida.com`, Nginx reverse proxy, PM2 process manager, Docker (PostgreSQL)
- **Optional AI:** Anthropic Claude (for photo analysis in Phase 5)

### Infrastructure Isolation
This app is **separate from the existing MG stack** (Medusa, ERPNext, Minio, NocoDB):
- Runs on its own port (8001)
- Has its own database
- Independent deployment and lifecycle
- Only integrates with Medusa API for product data

## Database Schema

### `users` table
- `id` (primary key)
- `email` (unique)
- `created_at`
- `newsletter_consent`

### `responses` table
- `id`, `user_id` (foreign key)
- `hair_color`, `skin_tone`, `eye_color`, `vein_color`, `jewelry_preference`
- `colors_worn` (JSON), `colors_avoided` (JSON)
- `submitted_at`

### `palettes` table
- `id`, `user_id` (foreign key)
- `season` (Spring/Summer/Autumn/Winter)
- `undertone` (warm/cool/neutral)
- `contrast_level` (high/medium/low)
- `core_neutrals` (JSON), `accent_colors` (JSON), `avoid_colors` (JSON)
- `generated_at`

### `photo_analyses` table (Phase 5 only)
- `id`, `user_id` (foreign key)
- `photo_path`, `refined_season`, `ai_analysis` (JSON)
- `analyzed_at`

## Color Season Analysis Logic

The questionnaire uses a **12-season system** (not 4!) with rule-based algorithm defined in YAML files.

### System Overview
- **Rules defined in:** `rules/` directory (questionnaire.yaml, seasons.yaml, mapping-rules.yaml)
- **Algorithm:** Signal accumulation → Characteristic determination → Season mapping
- **Seasons:** 12 total (Bright/True/Light Spring, Light/True/Soft Summer, Soft/True/Dark Autumn, Dark/True/Bright Winter)

### How It Works

1. **Signal Accumulation**: Each questionnaire answer adds weighted signals
   - Undertone signals: warm, cool, neutral
   - Value signals: light, medium, deep
   - Chroma signals: bright, muted, soft, rich
   - Contrast signals: high, medium, low

2. **Characteristic Determination**: Dominant signals determine characteristics
   - Vein color has highest weight (4) for undertone
   - Skin tone determines value
   - Color preferences indicate chroma

3. **Season Mapping**: Characteristics map to specific season
   - Example: Warm + Light + Soft = Light Spring
   - Example: Cool + Deep + Bright = Dark Winter

4. **Confidence Score**: Algorithm calculates 0-100% confidence
   - Boosts for aligned characteristics
   - Penalties for conflicts
   - Season-specific modifiers

Each season includes:
- Core neutrals (with hex codes)
- Accent colors (with hex codes)
- Colors to avoid
- Characteristics (undertone, value, chroma)

## Product Recommendation System

MG products should be tagged with:
- `primary_color`
- `temperature`: warm/cool/neutral
- `intensity`: bright/muted/deep
- `season_compatibility`: [Spring, Summer, Autumn, Winter]

Match user's determined season to compatible products from Medusa API.

## Development Phases

1. **Phase 1:** ✅ COMPLETE - Core questionnaire logic + PostgreSQL database
2. **Phase 2:** ✅ COMPLETE - Email integration with Resend, HTML email templates
3. **Phase 3:** 🚧 NEXT - Product recommendations from Medusa API
4. **Phase 4:** 📋 PLANNED - VPS deployment with subdomain, Nginx, SSL, PM2
5. **Phase 5:** 📋 PLANNED - Optional photo upload + AI analysis for refined recommendations
6. **Phase 6:** 📋 PLANNED - Analytics (completion rate, email opens, click-throughs)

### Phase 1 & 2 Status (COMPLETE)
- ✅ 12-season color analysis algorithm (YAML-based rules)
- ✅ FastAPI backend with auto-reload
- ✅ PostgreSQL database (Docker) with SQLAlchemy ORM
- ✅ Beautiful questionnaire with MG design system
- ✅ Email service integration (Resend)
- ✅ HTML email template with color swatches
- ✅ Local development environment fully working
- ✅ Code on GitHub (clean history, no secrets)

## Environment Variables

### Local Development (.env)
```bash
# Database (Docker PostgreSQL)
DATABASE_URL=postgresql://palette:palette@localhost:5433/palette

# Email Service (Resend)
RESEND_API_KEY=your_resend_test_key
FROM_EMAIL=ciao@maisonguida.com

# Medusa API (local or production)
MEDUSA_API_URL=http://localhost:9000
MEDUSA_PUBLISHABLE_KEY=your_local_publishable_key

# Optional: AI for photo analysis (Phase 5)
ANTHROPIC_API_KEY=your_claude_api_key

# App Settings
APP_PORT=8001
DEBUG=true
```

### Production VPS (.env)
```bash
# Database (Docker PostgreSQL on VPS)
DATABASE_URL=postgresql://palette:supersecurepassword@localhost:5433/palette

# Email Service (Resend)
RESEND_API_KEY=your_resend_production_key
FROM_EMAIL=ciao@maisonguida.com

# Medusa API (production)
MEDUSA_API_URL=https://api.maisonguida.it
MEDUSA_PUBLISHABLE_KEY=pk_c84c6c1d1424f1f17c09947321b854055c97c91d42e397ca2b3379f55e2fa9c6

# Optional: AI for photo analysis (Phase 5)
ANTHROPIC_API_KEY=your_claude_api_key

# App Settings
APP_PORT=8001
DEBUG=false
```

## Key Design Decisions

- **No framework frontend:** Keep it simple, fast, accessible
- **Email-first results:** Drive engagement and capture leads
- **Progressive enhancement:** Start with questionnaire, add photo analysis later
- **Standalone architecture:** Independent from MG's e-commerce stack for easier iteration
- **Privacy-conscious:** Clear consent for newsletter, GDPR compliance for EU users

## File Structure

```
palette-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── models.py               # Database models (SQLAlchemy)
│   ├── database.py             # Database connection & session
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── config.py               # Environment config (pydantic-settings)
│   ├── questionnaire.py        # Season determination algorithm
│   ├── email_service.py        # Resend email integration
│   ├── rules_loader.py         # YAML rules loader
│   └── product_matcher.py      # Medusa API integration (Phase 3)
├── rules/
│   ├── README.md               # Rules system documentation
│   ├── questionnaire.yaml      # Questions with weighted signals
│   ├── seasons.yaml            # 12 season definitions with hex codes
│   ├── mapping-rules.yaml      # Signal → season decision tree
│   └── system.md               # Philosophy and overview
├── static/
│   ├── css/style.css           # MG design system
│   └── js/questionnaire.js     # Form handling
├── templates/
│   ├── questionnaire.html      # Main questionnaire page
│   └── thank-you.html          # Confirmation page
├── email_templates/
│   └── palette-result.html     # Email with color swatches
├── docs/
│   ├── local-development.md    # Dev setup guide
│   ├── tech-plan.md            # Original planning doc
│   └── customer-question-list.md
├── requirements.txt            # Python dependencies
├── .env                        # Local environment variables (gitignored)
├── .env.example                # Template for environment setup
├── .gitignore
├── docker-compose.yml          # PostgreSQL for local dev
├── run.py                      # Development server script
└── CLAUDE.md                   # This file
```

## Success Metrics

- Questionnaire completion rate > 70%
- Email delivery rate > 95%
- Email open rate > 25%
- Product click-through rate > 10%
- Newsletter signup rate > 50%
