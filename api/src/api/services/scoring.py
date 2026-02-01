import numpy as np
from datetime import datetime
from collections import defaultdict
from ..config import ALERT_THRESHOLD, VOLUME_FACTOR

def generate_alerts(messages: list) -> list:
    """Generate alerts based on hourly sentiment scores."""
    if not messages:
        return []

    # Agrupar por hora
    hourly_data = defaultdict(lambda: {'scores': [], 'count': 0})
    
    for msg in messages:
        # Converter timestamp para datetime se necessário
        if isinstance(msg['timestamp'], str):
            timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
        else:
            timestamp = msg['timestamp']
        
        # Truncar para hora (remover minutos e segundos)
        hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
        
        hourly_data[hour_key]['scores'].append(msg['proba_resenha'])
        hourly_data[hour_key]['count'] += 1
    
    # Calcular métricas e gerar alertas
    alerts = []
    
    for hour, data in sorted(hourly_data.items()):
        mean_score = np.mean(data['scores'])
        count = data['count']
        
        # Fórmula M
        M = 0.7 * mean_score + 0.3 * (1 - np.exp(-count / VOLUME_FACTOR))
        
        if M >= ALERT_THRESHOLD:
            alerts.append({
                "hour": hour.strftime("%H:%M"),
                "score": round(M, 2),
                "message": "🍻 RESENHA DETECTADA"
            })
    
    return alerts