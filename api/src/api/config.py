from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Data paths (legacy, for migration)
DATA_DIR = Path("data")
MESSAGES_FILE = DATA_DIR / "messages.jsonl"
ALERTS_FILE = DATA_DIR / "alerts.json"
RANKING_FILE = DATA_DIR / "ranking.json"

# Model paths
MODELS_DIR = Path("modelos")
VECTORIZER_PATH = MODELS_DIR / "vetorizador.pkl"
MODEL_PATH = MODELS_DIR / "modelo_resenha.pkl"

# WhatsApp Group ID
GROUP_ID = os.getenv("GROUP_ID", "120363025949767428@g.us")

# Scoring thresholds
ALERT_THRESHOLD = 0.6
VOLUME_FACTOR = 20

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/sentimental_db")