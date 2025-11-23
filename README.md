# PALETTE-AI

Personal color analysis tool for [Maison Guida](https://maisonguida.com) - Determine your color season and receive personalized palette recommendations.

## Overview

PALETTE-AI helps users discover their personal color season through an interactive questionnaire, then delivers a curated color palette via email with product recommendations from the Maison Guida collection.

**Current Status:** Phase 1 & 2 Complete ✅

### Features

- ✅ **12-Season Color Analysis** - Advanced algorithm using warm/cool undertones, value depth, and chroma intensity
- ✅ **Smart Questionnaire** - 8 questions with weighted signal system (normalized for multi-select)
- ✅ **Email Delivery** - Beautiful HTML emails with color swatches and hex codes (Gmail/Outlook compatible)
- ✅ **GDPR Compliant** - Personal data collection with privacy consent
- ✅ **Black Box Testing** - 5 diverse test personas with 100% accuracy
- ✅ **Maison Guida Design** - Clean, minimalist UI matching the brand aesthetic
- ✅ **Analytics** - Plausible integration for cookieless tracking
- 🚧 **Product Recommendations** - Coming in Phase 3
- 📋 **Photo Analysis** - Planned for Phase 5

## Technology

- **Backend:** FastAPI (Python 3.11+), SQLAlchemy ORM, Alembic migrations
- **Database:** PostgreSQL (Docker)
- **Email:** Resend API with premailer for CSS inlining
- **Analytics:** Plausible (self-hosted, cookieless)
- **Frontend:** Vanilla HTML/CSS/JS (no framework)
- **Testing:** Black box testing with persona-based validation
- **Deployment:** PM2 + Nginx on VPS (planned)

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Resend API key (free tier available)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/JohnWatkinson/PALETTE-AI.git
cd PALETTE-AI

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your RESEND_API_KEY
# Set TESTING_MODE=true to disable emails during development

# 5. Start PostgreSQL
docker compose up -d

# 6. Run database migrations
alembic upgrade head

# 7. Run the app
python run.py
```

Visit **http://localhost:8001** to see the questionnaire!

### Running Tests

```bash
# Run black box tests with test personas
# Make sure server is running first!
source .venv/bin/activate
python testing/test_personas.py
```

## Project Structure

```
palette-ai/
├── app/                    # FastAPI application
│   ├── main.py            # App entry point
│   ├── questionnaire.py   # Season determination algorithm
│   ├── email_service.py   # Resend integration
│   ├── models.py          # Database models
│   └── config.py          # Environment settings
├── rules/                 # YAML-based color analysis rules
│   ├── questionnaire.yaml # Questions with signal weights
│   ├── seasons.yaml       # 12 season definitions
│   └── mapping-rules.yaml # Decision tree logic
├── testing/               # Black box tests
│   └── test_personas.py   # 5 test personas
├── migrations/            # Alembic database migrations
├── templates/             # HTML pages
├── email_templates/       # Email templates
└── static/               # CSS & JavaScript
```

## The 12 Seasons

The app uses a comprehensive 12-season color analysis system:

### Spring Family (Warm Undertones)
- **Bright Spring** - Clear, vibrant warm colors
- **True Spring** - Fresh, classic warm palette
- **Light Spring** - Delicate, soft warm tones

### Summer Family (Cool Undertones)
- **Light Summer** - Soft, airy cool colors
- **True Summer** - Elegant muted cool palette
- **Soft Summer** - Very muted, subtle cool tones

### Autumn Family (Warm Undertones)
- **Soft Autumn** - Gentle, earthy warm colors
- **True Autumn** - Rich, classic autumn palette
- **Dark Autumn** - Deep, intense warm tones

### Winter Family (Cool Undertones)
- **Dark Winter** - Deep, dramatic cool colors
- **True Winter** - Bright, icy cool palette
- **Bright Winter** - Maximum intensity cool tones

Each season includes:
- Core neutrals (4 colors with hex codes)
- Accent colors (6 colors with hex codes)
- Colors to avoid

## How It Works

1. **User completes questionnaire** (8 questions about physical characteristics and preferences)
2. **Algorithm accumulates signals** from responses (warm/cool, light/deep, bright/muted)
3. **Season is determined** using YAML-based decision tree
4. **Confidence score calculated** (0-100%)
5. **Email sent** with personalized palette and product recommendations
6. **Results saved** to PostgreSQL database

## Development

See [docs/local-development.md](docs/local-development.md) for detailed development guide.

### Key Commands

```bash
# Start development server (auto-reload enabled)
python run.py

# Run database migrations
alembic upgrade head

# Run tests (server must be running)
python testing/test_personas.py

# View API documentation
# Visit http://localhost:8001/docs

# Stop PostgreSQL
docker compose down
```

## API Endpoints

- `GET /` - Questionnaire page
- `POST /api/submit` - Submit questionnaire (returns PaletteResult)
- `GET /api/palette/{email}` - Get user's latest palette
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Deployment

Deployment to VPS planned for Phase 4:
- Subdomain: `palette.maisonguida.com`
- Process manager: PM2
- Reverse proxy: Nginx with SSL
- Database: Docker PostgreSQL on VPS

See [docs/tech-plan.md](docs/tech-plan.md) for full deployment plan.

## Roadmap

- [x] **Phase 1** - Core questionnaire & season algorithm
- [x] **Phase 2** - Email integration with Resend
- [ ] **Phase 3** - Product recommendations from Medusa API
- [ ] **Phase 4** - VPS deployment
- [ ] **Phase 5** - Photo upload & AI analysis
- [ ] **Phase 6** - Analytics & tracking

## Contributing

This is a private project for Maison Guida. For questions or issues, contact the development team.

## License

Proprietary - Maison Guida © 2025

---

**Built with:** FastAPI • PostgreSQL • Resend • Docker
**Designed for:** [Maison Guida](https://maisonguida.com)
