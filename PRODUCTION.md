# Ramadan Timetable 1447 AH - Production Setup

## Environment Variables

### Local Development (`.env`)
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=your-local-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Production (Render)
Set these environment variables in **Render Dashboard → Environment**:

| Variable | Value | Notes |
|----------|-------|-------|
| `DJANGO_DEBUG` | `false` | Must be false in production |
| `DJANGO_SECRET_KEY` | Generate strong secret | Use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DJANGO_ALLOWED_HOSTS` | Your Render domain | e.g., `ramadan-timetable.onrender.com` |
| `DATABASE_URL` | PostgreSQL URL from Render | From your PostgreSQL database |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://yourdomain.onrender.com` | Must match domain |
| `DJANGO_SECURE_SSL_REDIRECT` | `true` | Force HTTPS |
| `DJANGO_SESSION_COOKIE_SECURE` | `true` | Secure cookies |
| `DJANGO_CSRF_COOKIE_SECURE` | `true` | CSRF security |
| `TZ` | `Asia/Kolkata` | Timezone |

## Deployment on Render

### Option 1: Using `render.yaml` (One-Click)
```bash
git push
```
Render will auto-detect `render.yaml` and deploy.

### Option 2: Manual Setup
1. **Create Web Service**
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn ramadan_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2`

2. **Create PostgreSQL Database**
   - Render → New → PostgreSQL
   - Copy Internal Database URL

3. **Set Environment Variables** (see table above)

4. **Deploy**
   - Trigger deploy

5. **Post-Deploy**
   ```bash
   # In Render Shell:
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Local Development

### Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver
```

Visit: `http://localhost:8000`

## Security Checklist

- [x] `DEBUG=false` in production
- [x] `DJANGO_SECRET_KEY` is strong and random
- [x] `ALLOWED_HOSTS` configured for your domain
- [x] HTTPS enforced (`SECURE_SSL_REDIRECT=true`)
- [x] Secure cookies enabled
- [x] HSTS enabled
- [x] CSRF protection active
- [x] CORS restricted (not allow-all in prod)
- [x] Database connection secured
- [x] Static files collected
- [x] Logging configured

## Common Issues

### `DATABASE_URL is required in production`
Set `DATABASE_URL` in Render environment variables.

### Static files not loading
Run: `python manage.py collectstatic --noinput`

### CSRF errors
Ensure `DJANGO_CSRF_TRUSTED_ORIGINS` matches your domain.

### Secret key error on startup
Generate and set `DJANGO_SECRET_KEY` in environment.

## Tech Stack

- **Django 5.2** - Web framework
- **Django REST Framework** - API
- **PostgreSQL** - Database
- **Gunicorn** - WSGI server
- **WhiteNoise** - Static file serving
- **dj-database-url** - Database config
- **django-cors-headers** - CORS support

## Admin Panel

Access at: `https://yourdomain.onrender.com/admin`

## API Endpoints

- `GET /api/today/` - Today's timetable
- `GET /api/schedule/` - Full month schedule
- `GET /api/day/<day_number>/` - Specific day
- `GET /api/countdown/` - Iftar countdown
- `GET /api/settings/` - Site settings

---

**Last Updated**: February 18, 2026
