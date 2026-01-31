import numpy as np
import pandas as pd
from ..config import ALERT_THRESHOLD, VOLUME_FACTOR

def generate_alerts(df: pd.DataFrame) -> list:
    """Generate alerts based on hourly sentiment scores."""
    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"], format='mixed', utc=True)

    df_hourly = (
        df.groupby(pd.Grouper(key="timestamp", freq="60min"))
        .agg(
            mean_score=("proba_resenha", "mean"),
            count=("proba_resenha", "count")
        )
        .reset_index()
    )

    df_hourly["M"] = (
        0.7 * df_hourly["mean_score"]
        + 0.3 * (1 - np.exp(-df_hourly["count"] / VOLUME_FACTOR))
    )

    alerts = []
    for _, row in df_hourly.iterrows():
        if row.M >= ALERT_THRESHOLD:
            alerts.append({
                "hour": row.timestamp.strftime("%H:%M"),
                "score": round(row.M, 2),
                "message": "🍻 RESENHA DETECTADA"
            })

    return alerts
