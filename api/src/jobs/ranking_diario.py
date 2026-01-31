import json
import pandas as pd
import numpy as np
from datetime import date
from ..api.config import MESSAGES_FILE, RANKING_FILE, VOLUME_FACTOR

df = pd.read_json(MESSAGES_FILE, lines=True)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["data"] = df["timestamp"].dt.date

df = df[df["data"] == date.today()]

if df.empty:
    exit()

ranking = (
    df.groupby("sender")
    .agg(
        I=("proba_resenha", "mean"),
        n=("proba_resenha", "count")
    )
    .reset_index()
)

ranking["V"] = 1 - np.exp(-ranking["n"] / VOLUME_FACTOR)
ranking["M"] = 0.7 * ranking["I"] + 0.3 * ranking["V"]

top3 = ranking.sort_values("M", ascending=False).head(3)

output = []
for _, r in top3.iterrows():
    output.append({
        "sender": r.sender,
        "score": round(r.M, 2),
        "messages": int(r.n)
    })

with open(RANKING_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
