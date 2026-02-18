# Ramadan Timetable 1447 AH

Beautiful, multilingual Ramadan prayer timetable app with download & sharing.

## Features

- 📅 Full Ramadan schedule (30 days)
- 🕌 Sehri & Iftar times
- 🇵🇰 Multi-language (English, Urdu, Hindi)
- ⬇️ Download timetable cards as images
- 📤 Share cards on social media
- ⏳ Live Iftar countdown
- 🎨 Elegant dark theme with gold accents
- 📱 Fully responsive design
- 🔒 Production-ready security

## Quick Start

### Development
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: `http://localhost:8000`

### Production (Render)
See [PRODUCTION.md](PRODUCTION.md) for complete deployment guide.

## Admin Panel

- URL: `/admin`
- Add/edit Ramadan days
- Manage site settings (location, organization name, social handle)

## Tech Stack

- Django 5.2
- Django REST Framework
- PostgreSQL
- Gunicorn + WhiteNoise
- HTML5Canvas (for image downloads)

## License

MIT - Free to use and modify

## Support

For issues or questions, visit the admin panel or check logs.

---

**Ramadan Mubarak** 🌙 رمضان مبارک
