```markdown
# Color Analysis App - Development Plan

## Project Overview
Build a color palette recommendation tool for Maison Guida that captures emails, provides personalized color analysis via questionnaire, and recommends products from MG catalog.

## Goals
1. Capture emails for newsletter
2. Provide valuable color analysis to users
3. Recommend MG products based on user's color palette
4. Optional: Advanced photo analysis for deeper engagement
5. Learn VPS deployment and web app management

## Tech Stack

### Backend
- **FastAPI** (Python web framework)
- **SQLite** (database for emails, responses, palettes) - use postgres (medusa and everything else does)
- **Uvicorn** (ASGI server)
- **Pillow** (future: photo analysis)
- **Resend** (email delivery)
- Docker


### Frontend
- **HTML/CSS/JavaScript** (simple, no framework)
- **Optional: htmx** (for smooth interactions without heavy JS)

### Deployment
- **VPS** (existing server)
- **Nginx** (reverse proxy)
- **Systemd** (service management)
- **Subdomain:** colors.maisonguida.com

### Separate from existing stack
- Independent from Medusa, ERPNext, Minio, NocoDB
- Own process, own port, own database

## Phase 1: Core Questionnaire ✅ COMPLETE

### Tasks
- [x] Set up FastAPI project structure
- [x] Create PostgreSQL database schema (users, responses, palettes)
- [x] Build questionnaire logic (12-season system with YAML rules)
- [x] Create simple HTML questionnaire form (MG design system)
- [x] Implement season determination algorithm
- [x] Generate color palette based on season (with hex codes)
- [x] Store email + responses in database

### Deliverable
✅ Working questionnaire that determines user's season (12 seasons) and stores data

**Completed:** November 15, 2025

## Phase 2: Email Integration ✅ COMPLETE

### Tasks
- [x] Set up Resend account
- [x] Design HTML email template for palette results
- [x] Create color palette visual with hex swatches (inline CSS for email compatibility)
- [x] Implement email sending after questionnaire completion
- [x] Test email delivery (Resend working)
- [x] Add confirmation page after submission

### Deliverable
✅ Users receive personalized color palette via email after completing questionnaire

**Completed:** November 15, 2025

## Phase 3: Product Recommendations (Week 2)

### Tasks
- [ ] Tag MG products with color attributes (warm/cool, season compatibility)
- [ ] Build logic to match user's season → MG products
- [ ] Fetch product data from Medusa API
- [ ] Add product recommendations to email template
- [ ] Include product images and links
- [ ] Test product recommendation accuracy

### Deliverable
Email includes 3-5 relevant MG product recommendations with images and links

## Phase 4: Deployment (Week 2-3)

### Tasks
- [ ] Set up subdomain (colors.maisonguida.com)
- [ ] Configure nginx reverse proxy
- [ ] Create systemd service for FastAPI app
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Test deployment and server startup
- [ ] Monitor logs and fix any issues
- [ ] Set up basic error logging

### Deliverable
Live app running on VPS, accessible via subdomain

## Phase 5: Photo Upload (Optional - Week 3-4)

### Tasks
- [ ] Add "upgrade" CTA in email
- [ ] Create photo upload page
- [ ] Implement image storage (local or Minio)
- [ ] Integrate Claude/OpenAI Vision API for analysis
- [ ] Enhance color palette based on photo
- [ ] Send follow-up email with refined results
- [ ] Handle privacy/GDPR considerations

### Deliverable
Users can upload photos for enhanced color analysis

## Phase 6: Analytics & Optimization (Ongoing)

### Tasks
- [ ] Track questionnaire completion rate
- [ ] Monitor email open rates
- [ ] Track click-throughs to products
- [ ] A/B test email templates
- [ ] Analyze which seasons convert best
- [ ] Refine product recommendations based on data
- [ ] Add newsletter integration

### Deliverable
Data-driven insights to improve conversion

## File Structure

```
color-app/
├── main.py                 # FastAPI app entry point
├── models.py              # Database models
├── questionnaire.py       # Season mapping logic
├── email_service.py       # Email sending logic
├── product_matcher.py     # MG product recommendation logic
├── config.py              # Configuration (API keys, etc)
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── questionnaire.js
│   └── images/
│       └── color-swatches/
├── templates/
│   ├── questionnaire.html
│   ├── thank-you.html
│   └── photo-upload.html
├── email_templates/
│   ├── palette-result.html
│   └── photo-result.html
└── database.db           # SQLite database
```

## Database Schema

### users table
- id (primary key)
- email (unique)
- created_at
- newsletter_consent

### responses table
- id (primary key)
- user_id (foreign key)
- hair_color
- skin_tone
- eye_color
- vein_color
- jewelry_preference
- colors_worn (JSON)
- colors_avoided (JSON)
- submitted_at

### palettes table
- id (primary key)
- user_id (foreign key)
- season (Spring/Summer/Autumn/Winter)
- undertone (warm/cool/neutral)
- contrast_level (high/medium/low)
- core_neutrals (JSON)
- accent_colors (JSON)
- avoid_colors (JSON)
- generated_at

### photo_analyses table (optional, phase 5)
- id (primary key)
- user_id (foreign key)
- photo_path
- refined_season
- ai_analysis (JSON)
- analyzed_at

## Environment Variables / Config

```
# Email Service
EMAIL_API_KEY=your_resend_or_mailgun_key
FROM_EMAIL=ciao@maisonguida.com

# Medusa API (for product recommendations)
MEDUSA_API_URL=https://maisonguida.com/store
MEDUSA_API_KEY=your_medusa_api_key

# Optional: AI for photo analysis
ANTHROPIC_API_KEY=your_claude_api_key

# App Settings
APP_PORT=8001
DATABASE_URL=sqlite:///./database.db
```

## Success Metrics

### Phase 1-2
- Questionnaire completion rate > 70%
- Email delivery rate > 95%
- Email open rate > 25%

### Phase 3-4
- Product click-through rate > 10%
- Newsletter signup rate > 50%
- App uptime > 99%

### Phase 5-6
- Photo upload conversion > 15%
- Overall email → sale conversion > 2%

## Risk Mitigation

### Technical Risks
- **Email deliverability:** Use established service (Resend/Mailgun), warm up domain
- **Server resources:** Monitor CPU/memory, optimize if needed
- **Security:** Validate inputs, sanitize uploads, rate limit submissions

### Business Risks
- **Low engagement:** A/B test questionnaire length, email design
- **Privacy concerns:** Clear privacy policy, GDPR compliance for EU users
- **Product mismatch:** Regularly review and refine season → product mapping

## Next Steps

1. Review this plan with Paola
2. Set up development environment
3. Start Phase 1 with Claude Code
4. Deploy MVP (Phases 1-4) before adding photo analysis
5. Gather feedback from initial users
6. Iterate based on data

## Future Enhancements (Post-Launch)

- Social sharing of color palettes
- Seasonal wardrobe guides
- Virtual try-on with MG products
- Integration with MG physical shop (QR code in store)
- Referral system (share with friends)
- Premium tier with personal stylist consultation
```
