# RCMP123 Marketplace (FastAPI + Stripe)

## Backend

cd backend
python -m venv venv
venv\Scripts\activate  (Windows)
pip install -r requirements.txt

Set environment:

- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET

Run backend:

uvicorn app:app --reload --host 0.0.0.0 --port 8000

## Frontend

Open frontend/index.html in your browser.

## Notes

- Images stored in backend/images/
- SQLite DB at backend/rcmp123.db (auto-created)
