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

The questionnaire maps user responses to one of four color seasons:

### 1. Determine Undertone
- **Warm:** Green veins, gold jewelry preference, golden/red hair, earth tones
- **Cool:** Blue/purple veins, silver jewelry, ash blonde/black hair, blues/grays
- **Neutral:** Blue-green veins, both metals work, mixed preferences

### 2. Determine Contrast Level
- **High:** Very fair + dark hair, or deep skin + very dark hair, wears black/white/bright colors
- **Medium:** Most combinations, mix of bright and muted
- **Low:** Fair + light hair, or medium skin + medium hair, prefers soft/muted colors

### 3. Season Mapping
- **SPRING** (Warm + Bright): Coral, peach, bright yellow, turquoise, warm green
- **SUMMER** (Cool + Soft): Soft pink, lavender, powder blue, mauve, cocoa
- **AUTUMN** (Warm + Muted): Rust, olive, terracotta, burnt orange, deep teal
- **WINTER** (Cool + Bright): True red, royal blue, emerald, pure white, black, magenta

Each season provides core neutrals, accent colors, and colors to avoid.

## Product Recommendation System

MG products should be tagged with:
- `primary_color`
- `temperature`: warm/cool/neutral
- `intensity`: bright/muted/deep
- `season_compatibility`: [Spring, Summer, Autumn, Winter]

Match user's determined season to compatible products from Medusa API.

## Development Phases

1. **Phase 1:** Core questionnaire logic + PostgreSQL database from the start
2. **Phase 2:** Email integration with Resend, HTML email templates
3. **Phase 3:** Product recommendations from Medusa API
4. **Phase 4:** VPS deployment with subdomain, Nginx, SSL, systemd
5. **Phase 5:** Optional photo upload + AI analysis for refined recommendations
6. **Phase 6:** Analytics (completion rate, email opens, click-throughs)

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
│   ├── main.py                 # FastAPI entry point
│   ├── models.py               # Database models (SQLAlchemy)
│   ├── database.py             # Database connection
│   ├── schemas.py              # Pydantic schemas
│   ├── config.py               # Environment config
│   ├── questionnaire.py        # Season determination logic
│   ├── email_service.py        # Resend integration
│   └── product_matcher.py      # Medusa API integration
├── static/
│   ├── css/style.css
│   ├── js/questionnaire.js
│   └── images/color-swatches/
├── templates/
│   ├── questionnaire.html
│   ├── thank-you.html
│   └── photo-upload.html       # Phase 5
├── email_templates/
│   ├── palette-result.html
│   └── photo-result.html       # Phase 5
├── requirements.txt
├── .env                        # Local environment variables
├── .env.example                # Template for environment setup
├── docker-compose.yml          # PostgreSQL for local dev
└── ecosystem.config.js         # PM2 config for VPS deployment
```

## Success Metrics

- Questionnaire completion rate > 70%
- Email delivery rate > 95%
- Email open rate > 25%
- Product click-through rate > 10%
- Newsletter signup rate > 50%
