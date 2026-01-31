import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from ..api.config import MESSAGES_FILE, ALERTS_FILE, ALERT_THRESHOLD, VOLUME_FACTOR
import numpy as np

# Load messages
df = pd.read_json(MESSAGES_FILE, lines=True)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Get last 2 hours
now = datetime.now()
df = df[df["timestamp"] >= now - timedelta(hours=2)]

if df.empty:
    exit()

# Scoring per interval
df_hourly = (
    df.groupby(pd.Grouper(key="timestamp", freq="1H"))
    .agg(
        I=("proba_resenha", "mean"),
        n=("proba_resenha", "count")
    )
    .reset_index()
)

df_hourly["V"] = 1 - np.exp(-df_hourly["n"] / VOLUME_FACTOR)
df_hourly["M"] = 0.7 * df_hourly["I"] + 0.3 * df_hourly["V"]

# Detect alerts
alerts = []
for _, row in df_hourly.iterrows():
    if row.M >= ALERT_THRESHOLD:
        alerts.append({
            "timestamp": row.timestamp.isoformat(),
            "score": round(row.M, 2),
            "message": f"🍻 RESENHA DETECTADA\nScore: {row.M:.2f}"
        })

if not alerts:
    exit()

# Save latest alert
with open(ALERTS_FILE, "w", encoding="utf-8") as f:
    json.dump(alerts[-1], f, ensure_ascii=False, indent=2)
