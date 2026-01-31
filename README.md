# Sentiment Analysis API

FastAPI backend for sentiment analysis of WhatsApp messages.

## Structure

- `src/`: API code
- `modelos/`: Machine learning models (do not modify)
- `notebooks/`: Jupyter notebooks for model development and experimentation
- `requirements.txt`: Python dependencies
- `Dockerfile`: For deployment

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up database:
   - Create MySQL database.
   - Set environment variables in Railway (copy from `.env.example`): `DATABASE_URL` and `GROUP_ID`.
   - Run migration: `python migrate.py`

3. Run API:
   ```bash
   uvicorn src.api.main:app --reload
   ```

## Deployment

Deploy to Railway with MySQL add-on. Set `DATABASE_URL` env var.