# PALETTE-AI - Local Development Guide

## Quick Overview
A FastAPI-based color palette recommendation tool that:
- Captures emails through interactive questionnaire
- Determines user's color season using **12-season system** (not 4!)
- Sends personalized palette recommendations via Resend
- (Phase 3) Recommends Maison Guida products from Medusa API

**Current Status:** Phase 1 & 2 Complete ✅

## Development Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- pip/venv

### 1. Clone and Setup Virtual Environment
```bash
cd /home/john/AI/PALETTE-AI
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy example and add your keys
cp .env.example .env

# Edit .env and add:
# - RESEND_API_KEY (get from resend.com)
# - MEDUSA_PUBLISHABLE_KEY (optional, for Phase 3)
```

### 3. Start Infrastructure (PostgreSQL)
```bash
docker compose up -d  # Starts PostgreSQL on port 5433
```

### 4. Run Development Server
```bash
# Database tables are created automatically on startup!
python run.py

# Or directly with uvicorn:
uvicorn app.main:app --reload --port 8001
```

The app will:
- ✅ Auto-create database tables on first run
- ✅ Watch for code changes and reload
- ✅ Be available at http://localhost:8001

## Key URLs

- **Questionnaire**: http://localhost:8001 (Main user interface)
- **API Docs**: http://localhost:8001/docs (Swagger UI)
- **Health Check**: http://localhost:8001/health
- **PostgreSQL**: localhost:5433 (Database)

## Project Structure

```
palette-ai/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection & session
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── questionnaire.py     # Season determination algorithm
│   ├── email_service.py     # Resend email integration
│   └── product_matcher.py   # Medusa product recommendations
├── static/
│   ├── css/style.css        # Maison Guida design system
│   └── js/questionnaire.js  # Frontend interactivity
├── templates/
│   ├── questionnaire.html   # Main questionnaire page
│   └── thank-you.html       # Confirmation page
├── email_templates/
│   └── palette-result.html  # Email template (Resend)
├── docker-compose.yml       # PostgreSQL container
├── requirements.txt         # Python dependencies
└── .env                     # Local environment variables
```

## Development Workflow

### Making Changes
1. **Backend logic**: Edit files in `app/`, auto-reload enabled
2. **Frontend**: Edit `templates/` or `static/`, refresh browser
3. **Email templates**: Edit `email_templates/`, test via `/test-email` endpoint

### Database Operations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Reset database (nuclear option)
docker compose down -v
docker compose up -d
alembic upgrade head
```

### Testing Questionnaire Flow
```bash
# Submit test questionnaire
curl -X POST http://localhost:8001/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "hair_color": "golden_blonde",
    "skin_tone": "fair",
    "eye_color": "blue",
    "vein_color": "green",
    "jewelry_preference": "gold",
    "colors_worn": ["coral", "peach"],
    "colors_avoided": ["black", "navy"],
    "newsletter_consent": true
  }'
```

## Environment Variables

Create a `.env` file in the root:

```bash
# Database (local Docker)
DATABASE_URL=postgresql://palette:palette@localhost:5433/palette

# Email Service (get test key from resend.com)
RESEND_API_KEY=re_test_xxxxxxxxxxxxxxxxx
FROM_EMAIL=ciao@maisonguida.com

# Medusa API (point to local or production)
MEDUSA_API_URL=http://localhost:9000
MEDUSA_PUBLISHABLE_KEY=pk_your_local_key_here

# App Settings
APP_PORT=8001
DEBUG=true
```

## Useful Commands

### FastAPI
```bash
# Run with auto-reload
uvicorn app.main:app --reload --port 8001

# Run with specific host (for network access)
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Check routes
python -c "from app.main import app; print([r.path for r in app.routes])"
```

### Docker (PostgreSQL)
```bash
docker compose ps              # Check status
docker compose logs -f         # View logs
docker compose down            # Stop database
docker compose down -v         # Stop and delete volumes (fresh start)

# Access PostgreSQL CLI
docker exec -it palette-postgres psql -U palette -d palette
```

### Database Inspection
```sql
-- Inside PostgreSQL CLI
\dt                           -- List tables
\d users                      -- Describe users table
SELECT * FROM users LIMIT 5;  -- View data
```

## Testing Email Service

### Resend Test Mode
Sign up for free at [resend.com](https://resend.com):
- Free tier: 100 emails/day
- Test mode: Emails don't actually send (for development)
- Production mode: Real email delivery

### Test Email Endpoint
```bash
# Send test palette email
curl -X POST http://localhost:8001/api/test-email \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com", "season": "Spring"}'
```

## Season Determination Algorithm

The questionnaire uses a **12-season system** with YAML-based rules:

### How It Works

1. **Signal Accumulation**: Each answer adds weighted signals
   - Undertone: warm/cool/neutral (vein color has weight 4)
   - Value: light/medium/deep (from skin tone)
   - Chroma: bright/muted/soft/rich (from color preferences)
   - Contrast: high/medium/low

2. **Characteristic Determination**: Finds dominant signals
   - Warm undertone if warm signals >= 8
   - Light value if light signals >= 6
   - Bright chroma if bright signals >= 5

3. **Season Mapping**: Maps to one of 12 seasons
   - **Spring Family** (Warm): Bright Spring, True Spring, Light Spring
   - **Summer Family** (Cool): Light Summer, True Summer, Soft Summer
   - **Autumn Family** (Warm): Soft Autumn, True Autumn, Dark Autumn
   - **Winter Family** (Cool): Dark Winter, True Winter, Bright Winter

4. **Confidence Score**: 0-100% based on signal strength and modifiers

See `rules/` directory for complete algorithm details.

## Common Tasks

### Add New Question to Questionnaire
1. Update `schemas.py` → Add field to `QuestionnaireSubmission`
2. Update `models.py` → Add column to `Response` model
3. Update `questionnaire.py` → Incorporate into season logic
4. Update `templates/questionnaire.html` → Add form field
5. Run migration: `alembic revision --autogenerate -m "add new question"`

### Customize Color Palettes
Edit `questionnaire.py`:
```python
SEASON_PALETTES = {
    "Spring": {
        "core_neutrals": ["cream", "camel", "warm_gray"],
        "accent_colors": ["coral", "peach", "turquoise"],
        "avoid_colors": ["black", "navy", "burgundy"]
    },
    # ... add more
}
```

### Connect to Production Medusa API
Update `.env`:
```bash
MEDUSA_API_URL=https://api.maisonguida.it
MEDUSA_PUBLISHABLE_KEY=pk_c84c6c1d1424f1f17c09947321b854055c97c91d42e397ca2b3379f55e2fa9c6
```

## Design System

Uses Maison Guida design language:
- **Monochrome palette**: Black, white, warm grays
- **Typography**: Light font weights, generous spacing
- **Minimal UI**: Clean, luxury aesthetic (inspired by The Row)
- **No emojis**: Professional tone

## Git Workflow

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Add feature"

# Push to GitHub
git push origin master

# Pull latest
git pull origin master
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>
```

### Database Connection Failed
```bash
# Verify PostgreSQL is running
docker compose ps

# Check logs
docker compose logs palette-postgres

# Restart container
docker compose restart
```

### Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Email Not Sending
```bash
# Check Resend API key is valid
curl https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ciao@maisonguida.com",
    "to": "test@example.com",
    "subject": "Test",
    "html": "<p>Test email</p>"
  }'
```

## Next Steps for Production

- [ ] Get production Resend API key
- [ ] Set up subdomain: `palette.maisonguida.com`
- [ ] Configure Nginx reverse proxy
- [ ] Set up PM2 for process management
- [ ] Add SSL certificate (Let's Encrypt)
- [ ] Set up monitoring and logs
- [ ] Create systemd service for auto-start

## Production Deployment Preview

Similar to fashion-starter deployment:
```bash
# On VPS
ssh john@72.61.20.227
cd ~/palette-ai
git pull origin master
source venv/bin/activate
pip install -r requirements.txt
pm2 restart palette-api
pm2 save
```

See [vps-deployment.md](vps-deployment.md) for full deployment guide.

---

**Status**: ✅ Phase 1 & 2 Complete
**Current Phase**: Phase 3 - Product Recommendations (Next)
**Last Updated**: November 15, 2025
