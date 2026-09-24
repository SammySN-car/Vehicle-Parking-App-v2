# Vehicle Parking App — v2

Full-stack rewrite of the parking booking system: **Flask REST API** + **Vue 3 (Vite)** SPA, with JWT auth, SQLAlchemy models, Celery/Redis background CSV exports, and Flask-Mail password recovery.

## Features

- **JWT auth** — register/login; tokens in `Authorization: Bearer` headers
- **Admin** — lot/spot CRUD, user management, search, summary analytics
- **User** — book/release spots, profile edit, personal summary
- **Async CSV export** — Celery task compiles history; download via API
- **Mail** — Flask-Mail for account recovery flows
- **CORS** — locked to `http://localhost:5173` (Vite dev server)

## Tech stack

| Layer | Tech |
|-------|------|
| API | Flask 3, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy |
| Jobs | Celery + Redis |
| Mail | Flask-Mail (Gmail SMTP) |
| Frontend | Vue 3, Vue Router, Axios, Chart.js, Vite |
| DB | SQLite |

## Project layout

```
Vehicle-Parking-App-v2/
  Backend/
    app.py              # app factory, config, route registration
    routes/             # auth, lots, spots, search, summary, csv
    models/database.py  # SQLAlchemy models
    tasks/              # Celery tasks
    utils/              # db, jwt, redis helpers
    data/parking.db     # SQLite (gitignored)
  Frontend/
    src/                # Vue components, router, main.js
  .env                  # secrets (gitignored)
  requirements.txt
```

## Setup

### 1. Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment

Create `.env` in the project root (copy from `.env.example` values below):

```
JWT_SECRET_KEY=your-long-random-string
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_USE_TLS=False
MAIL_USE_SSL=True
```

> Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your login password. `.env` is gitignored.

### 3. Redis (for Celery)

```bash
redis-server
```

### 4. Frontend

```bash
cd Frontend
npm install
npm run dev
```

## Run

Terminal 1 — API:

```bash
python -m Backend.app
# → http://127.0.0.1:5000
```

Terminal 2 — Celery worker (optional, for CSV export):

```bash
celery -A Backend.celery_work worker --loglevel=info
```

Terminal 3 — frontend:

```bash
cd Frontend
npm run dev
# → http://localhost:5173
```

Default admin (seeded on first run): `ADMIN@gmail.com` / `admin`.

## API overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register`, `/` (login) | Auth |
| GET/POST | `/admin/home`, `/admin/add_lot`, … | Admin lots/spots |
| GET/POST | `/user/home`, `/user/book/<id>`, … | User bookings |
| GET | `/user/export_csv` | Kick off Celery CSV job |

Interactive docs: none by default (Flask-RESTful routes registered manually).

## License

For coursework / personal use.
