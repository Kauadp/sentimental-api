import numpy as np
import pandas as pd
from datetime import date
from ..config import VOLUME_FACTOR

def generate_daily_ranking(df) -> list:
    """Generate daily ranking of senders based on sentiment scores."""
    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"], format='mixed', utc=True)
    df_today = df[df["timestamp"].dt.date == date.today()]

    if df_today.empty:
        return []

    ranking = (
        df_today.groupby("sender")
        .agg(
            I=("proba_resenha", "mean"),
            n=("proba_resenha", "count")
        )
        .reset_index()
    )

    ranking["V"] = 1 - np.exp(-ranking["n"] / VOLUME_FACTOR)
    ranking["M"] = 0.7 * ranking["I"] + 0.3 * ranking["V"]

    ranking = ranking.sort_values("M", ascending=False)

    return ranking.to_dict(orient="records")
