# PALETTE-AI VPS Deployment Guide

**Server:** Hostinger VPS (same as Maison Guida main site)
**IP:** 72.61.20.227
**User:** john
**Subdomain:** https://palette.maisonguida.com
**Port:** 8001

---

## Quick Deployment (CODE CHANGES)

⚠️ **POST-LAUNCH**: For deploying code changes only (form updates, email templates, algorithm tweaks).

```bash
# 1. SSH into VPS
ssh john@72.61.20.227

# 2. Navigate to project
cd ~/PALETTE-AI

# 3. Pull latest changes from GitHub
git pull origin master

# 4. Restart PM2 service
pm2 restart palette-ai
pm2 save

# 5. Verify it's running
pm2 status
curl http://localhost:8001/

# 6. Monitor for issues
pm2 logs palette-ai --lines 50
```

**Important Notes:**
- No rebuild needed (FastAPI auto-reloads Python files in production)
- If requirements.txt changed, run: `pip install -r requirements.txt`
- If environment variables changed, restart is required
- Database migrations: `cd ~/PALETTE-AI && python -c "from app.database import init_db; init_db()"`

---

## Initial VPS Setup (First Deployment)

### 1. Prerequisites on VPS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y

# Install PM2 (if not already installed)
npm install -g pm2
```

### 2. Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/PALETTE-AI.git
cd PALETTE-AI
```

### 3. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database (Docker)

The PALETTE-AI app uses its own PostgreSQL database, separate from Medusa.

```bash
# Navigate to project
cd ~/PALETTE-AI

# Start PostgreSQL container
docker-compose up -d

# Verify container is running
docker ps | grep palette

# Create tables (run migrations)
python -c "from app.database import init_db; init_db()"
```

**Database runs on port 5433** (different from Medusa's 5432)

### 5. Configure Environment Variables

```bash
# Create production .env file
cd ~/PALETTE-AI
nano .env
```

**Production .env:**
```bash
# Database (Docker PostgreSQL on VPS)
DATABASE_URL=postgresql://palette:CHANGE_THIS_PASSWORD@localhost:5433/palette

# Email Service (Resend)
RESEND_API_KEY=YOUR_PRODUCTION_RESEND_KEY
FROM_EMAIL=ciao@maisonguida.com

# Medusa API (production)
MEDUSA_API_URL=https://api.maisonguida.it
MEDUSA_PUBLISHABLE_KEY=pk_c84c6c1d1424f1f17c09947321b854055c97c91d42e397ca2b3379f55e2fa9c6

# Optional: AI for photo analysis (Phase 5)
ANTHROPIC_API_KEY=YOUR_CLAUDE_API_KEY

# App Settings
APP_PORT=8001
DEBUG=false
```

**Security Notes:**
- Change `CHANGE_THIS_PASSWORD` to a strong password
- Never commit `.env` to Git
- Keep `.env.example` updated for reference

### 6. Configure PM2

Create PM2 ecosystem config:

```bash
cd ~/PALETTE-AI
nano ecosystem.config.js
```

```javascript
module.exports = {
  apps: [
    {
      name: 'palette-ai',
      script: 'venv/bin/python',
      args: '-m uvicorn app.main:app --host 0.0.0.0 --port 8001',
      cwd: '/home/john/PALETTE-AI',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
      },
      error_file: '/home/john/.pm2/logs/palette-ai-error.log',
      out_file: '/home/john/.pm2/logs/palette-ai-out.log',
      log_file: '/home/john/.pm2/logs/palette-ai-combined.log',
      time: true,
    },
  ],
};
```

Start the app:

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup  # Enable auto-start on reboot
```

### 7. Configure Nginx Reverse Proxy

Create Nginx config for subdomain:

```bash
sudo nano /etc/nginx/sites-available/palette_maisonguida_com
```

```nginx
server {
    listen 80;
    server_name palette.maisonguida.com;

    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;

    # Static files
    location /static/ {
        alias /home/john/PALETTE-AI/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # FastAPI app
    location / {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/palette_maisonguida_com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 8. Set Up DNS (Subdomain)

**On your domain registrar or DNS provider:**

Add an A record:
- **Host:** `palette`
- **Type:** `A`
- **Value:** `72.61.20.227`
- **TTL:** `3600` (or auto)

Wait for DNS propagation (5-30 minutes).

Test:
```bash
ping palette.maisonguida.com
# Should return 72.61.20.227
```

### 9. Set Up SSL Certificate (Let's Encrypt)

```bash
# Run Certbot
sudo certbot --nginx -d palette.maisonguida.com

# Follow prompts:
# - Enter email for renewal notices
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (recommended)
```

Certbot will:
- Obtain SSL certificate
- Automatically update Nginx config
- Set up auto-renewal

Verify:
```bash
sudo certbot renew --dry-run
```

### 10. Upload Static Assets

Upload your logo and other static files:

```bash
# From local machine
scp -r static/images/* john@72.61.20.227:~/PALETTE-AI/static/images/

# Or use SFTP/FileZilla
```

### 11. Test Deployment

```bash
# Check PM2 status
pm2 status

# Check logs
pm2 logs palette-ai --lines 50

# Test endpoints
curl http://localhost:8001/
curl http://localhost:8001/static/images/site-logo.svg

# Test from browser
# Visit: https://palette.maisonguida.com
```

---

## File Locations on VPS

- **Repo:** `~/PALETTE-AI/`
- **Virtual Environment:** `~/PALETTE-AI/venv/`
- **Database:** Docker container `palette-postgres` (port 5433)
- **PM2 Config:** `~/PALETTE-AI/ecosystem.config.js`
- **Nginx Config:** `/etc/nginx/sites-available/palette_maisonguida_com`
- **Static Files:** `~/PALETTE-AI/static/`
- **Email Templates:** `~/PALETTE-AI/email_templates/`
- **Logs:** `~/.pm2/logs/palette-ai-*.log`

---

## PM2 Commands

```bash
# Status
pm2 status

# Logs
pm2 logs palette-ai
pm2 logs palette-ai --lines 100
pm2 logs palette-ai --err  # Errors only

# Restart
pm2 restart palette-ai
pm2 restart all

# Stop
pm2 stop palette-ai

# Monitor
pm2 monit

# Save current process list
pm2 save
```

---

## Docker Commands (PostgreSQL)

```bash
cd ~/PALETTE-AI

# Status
docker ps | grep palette
docker-compose ps

# Logs
docker logs palette-postgres

# Restart
docker-compose restart

# Stop
docker-compose down

# Start
docker-compose up -d

# Access database
docker exec -it palette-postgres psql -U palette -d palette
```

---

## Database Management

### View Users
```bash
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT id, email, created_at, newsletter_consent FROM users ORDER BY created_at DESC LIMIT 10;"
```

### View Responses
```bash
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT COUNT(*) FROM responses;"
```

### View Palettes
```bash
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT season, COUNT(*) FROM palettes GROUP BY season ORDER BY COUNT(*) DESC;"
```

### Backup Database
```bash
# Create backup
docker exec palette-postgres pg_dump -U palette palette > ~/backups/palette-$(date +%Y%m%d).sql

# Restore backup
docker exec -i palette-postgres psql -U palette palette < ~/backups/palette-20250116.sql
```

### Run Migrations (if schema changes)
```bash
cd ~/PALETTE-AI
source venv/bin/activate
python -c "from app.database import init_db; init_db()"
```

---

## Monitoring & Analytics

### Check Questionnaire Submissions
```bash
# Total submissions
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT COUNT(*) as total_submissions FROM responses;"

# Submissions by date
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT DATE(submitted_at) as date, COUNT(*) as submissions FROM responses GROUP BY DATE(submitted_at) ORDER BY date DESC;"

# Most common seasons
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT season, COUNT(*) as count FROM palettes GROUP BY season ORDER BY count DESC;"

# Newsletter signups
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT COUNT(*) as newsletter_signups FROM users WHERE newsletter_consent = true;"
```

### Application Logs
```bash
# Real-time logs
pm2 logs palette-ai --lines 0

# Last 100 lines
pm2 logs palette-ai --lines 100

# Errors only
pm2 logs palette-ai --err
```

### Server Resources
```bash
# CPU/Memory usage
pm2 monit

# Disk usage
df -h

# Database size
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT pg_size_pretty(pg_database_size('palette'));"
```

---

## Troubleshooting

### App Not Loading (502 Error)
```bash
# Check PM2 status
pm2 status

# Check logs for errors
pm2 logs palette-ai --lines 50

# Restart app
pm2 restart palette-ai
pm2 save
```

### Database Connection Error
```bash
# Check container is running
docker ps | grep palette

# Restart container
cd ~/PALETTE-AI
docker-compose restart

# Check DATABASE_URL in .env matches container settings
cat .env | grep DATABASE_URL
```

### Email Not Sending
```bash
# Check logs for Resend errors
pm2 logs palette-ai | grep -i email

# Verify RESEND_API_KEY in .env
cat .env | grep RESEND_API_KEY

# Test Resend API key (from VPS)
curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"from":"ciao@maisonguida.com","to":"test@example.com","subject":"Test","html":"Test"}'
```

### Static Files Not Loading (Logo, CSS)
```bash
# Check files exist
ls -la ~/PALETTE-AI/static/images/

# Check Nginx config for static file location
sudo nano /etc/nginx/sites-available/palette_maisonguida_com

# Reload Nginx
sudo systemctl reload nginx

# Check file permissions
sudo chown -R john:john ~/PALETTE-AI/static/
chmod -R 755 ~/PALETTE-AI/static/
```

### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Check Nginx SSL config
sudo nano /etc/nginx/sites-available/palette_maisonguida_com
```

### Fresh Deployment (Nuclear Option)
```bash
# Stop app
pm2 stop palette-ai

# Backup database first!
docker exec palette-postgres pg_dump -U palette palette > ~/backups/palette-emergency-$(date +%Y%m%d-%H%M).sql

# Pull fresh code
cd ~/PALETTE-AI
git stash  # Save any VPS-only changes (.env)
git pull origin master

# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart app
pm2 restart palette-ai
pm2 save
```

---

## Security Checklist

- [ ] `.env` file has strong database password
- [ ] `.env` is in `.gitignore` (never committed)
- [ ] SSL certificate is active (HTTPS)
- [ ] Nginx configured to redirect HTTP → HTTPS
- [ ] Database only accessible from localhost (not exposed to internet)
- [ ] PM2 running as non-root user
- [ ] Regular database backups scheduled
- [ ] Resend API key is production key (not test)
- [ ] Rate limiting configured in FastAPI (prevent spam)
- [ ] CORS properly configured
- [ ] Server firewall configured (UFW)

---

## Deployment Checklist

### First-Time Setup
- [ ] Install prerequisites (Python, Nginx, Docker, PM2)
- [ ] Clone repository from GitHub
- [ ] Create Python virtual environment
- [ ] Install dependencies (`requirements.txt`)
- [ ] Start PostgreSQL container
- [ ] Create production `.env` file
- [ ] Run database migrations
- [ ] Configure PM2 ecosystem
- [ ] Set up Nginx reverse proxy
- [ ] Configure DNS (A record for subdomain)
- [ ] Obtain SSL certificate (Certbot)
- [ ] Upload static assets (logo, favicon)
- [ ] Test questionnaire flow
- [ ] Test email delivery
- [ ] Verify database storage

### Regular Deployment (Code Updates)
- [ ] SSH into VPS: `ssh john@72.61.20.227`
- [ ] Navigate to project: `cd ~/PALETTE-AI`
- [ ] Pull latest code: `git pull origin master`
- [ ] Check `.env` hasn't been overwritten
- [ ] Install new dependencies (if `requirements.txt` changed)
- [ ] Run migrations (if schema changed)
- [ ] Restart service: `pm2 restart palette-ai && pm2 save`
- [ ] Check logs: `pm2 logs palette-ai --lines 50`
- [ ] Test questionnaire: https://palette.maisonguida.com
- [ ] Test email delivery
- [ ] Clear browser cache and test in incognito

---

## Integration with Main Site

PALETTE-AI runs **independently** from the main Maison Guida e-commerce stack:

- **Separate database:** palette (port 5433) vs medusa (port 5432)
- **Separate process:** PM2 runs both independently
- **Separate subdomain:** palette.maisonguida.com vs shop.maisonguida.it
- **Shared VPS:** Same server, different ports
- **Medusa integration:** PALETTE-AI calls Medusa API for product recommendations (Phase 3)

**No conflicts!** Both apps can run side-by-side safely.

---

## Backup Strategy

### Automated Daily Backups
```bash
# Create backup script
nano ~/scripts/backup-palette-daily.sh
```

```bash
#!/bin/bash
BACKUP_DIR="$HOME/backups/palette"
DATE=$(date +%Y%m%d-%H%M)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
docker exec palette-postgres pg_dump -U palette palette > "$BACKUP_DIR/palette-db-$DATE.sql"

# Compress
gzip "$BACKUP_DIR/palette-db-$DATE.sql"

# Keep only last 30 days
find "$BACKUP_DIR" -name "palette-db-*.sql.gz" -mtime +30 -delete

echo "✅ Backup complete: $BACKUP_DIR/palette-db-$DATE.sql.gz"
```

```bash
# Make executable
chmod +x ~/scripts/backup-palette-daily.sh

# Add to crontab (runs daily at 3 AM)
crontab -e
# Add line:
0 3 * * * /home/john/scripts/backup-palette-daily.sh >> /home/john/logs/backup-palette.log 2>&1
```

### Manual Backup
```bash
# Quick manual backup
docker exec palette-postgres pg_dump -U palette palette > ~/palette-backup-$(date +%Y%m%d).sql
```

---

## Environment Variables Reference

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `RESEND_API_KEY` - Resend API key for emails
- `FROM_EMAIL` - Sender email (ciao@maisonguida.com)

### Optional (Phase 3+)
- `MEDUSA_API_URL` - Medusa backend URL
- `MEDUSA_PUBLISHABLE_KEY` - Medusa API key
- `ANTHROPIC_API_KEY` - Claude API for photo analysis (Phase 5)

### App Settings
- `APP_PORT` - Port to run on (default: 8001)
- `DEBUG` - Debug mode (false in production)

---

## Notes

- **PM2** auto-starts on VPS reboot
- **Docker containers** auto-start on reboot
- **SSL certificate** auto-renews via Certbot
- **Database** is isolated from main Medusa database
- **Static files** (logo, CSS) served by Nginx
- **Email templates** are rendered server-side with Jinja2
- **No framework frontend** - simple HTML/CSS/JS for fast loading

---

**Last Updated:** January 16, 2025
**Status:** 🚧 Ready for deployment
**Current Phase:** Phase 2 complete (questionnaire + email)
**Next Phase:** Phase 3 (product recommendations from Medusa API)

---

## Quick Reference Commands

```bash
# Deploy code changes
cd ~/PALETTE-AI && git pull && pm2 restart palette-ai

# Check status
pm2 status && docker ps | grep palette

# View logs
pm2 logs palette-ai --lines 50

# Backup database
docker exec palette-postgres pg_dump -U palette palette > ~/backup-$(date +%Y%m%d).sql

# Check submissions
docker exec -it palette-postgres psql -U palette -d palette -c "SELECT COUNT(*) FROM responses;"
```
