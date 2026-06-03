# Nava Nirman Backend

This folder contains a minimal Python backend for your website using FastAPI.

## Structure

- `app/main.py` — FastAPI application, routes, and page rendering
- `app/models.py` — SQLModel definitions for data objects
- `app/crud.py` — simple data access functions and seeded product/category data
- `app/database.py` — SQLite engine configuration
- `app/templates/` — HTML templates to serve (move your existing `.html` files here)
- `app/static/` — CSS, JS, and image assets (move `styles.css`, `script.js`, `images/` here)
- `requirements.txt` — Python dependencies for the backend

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

Build and run the backend with Docker:

```bash
cd backend
docker build -t nava-nirman-backend .
docker run --rm -p 8000:8000 nava-nirman-backend
```

## Procfile

A `Procfile` is included for Heroku-style deployments:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Next steps

1. Move your frontend pages into `backend/app/templates/`.
2. Update CSS/JS links in the templates to use `/static/styles.css` and `/static/script.js`.
3. Move your `images/` folder into `backend/app/static/images/`.
4. Add production database configuration once the site is working.
