import numpy as np
from datetime import date, datetime
from collections import defaultdict
from ..config import VOLUME_FACTOR

def generate_daily_ranking(messages: list) -> list:
    """Generate daily ranking of senders based on sentiment scores."""
    if not messages:
        return []
    
    # Filtrar mensagens de hoje
    today = date.today()
    messages_today = []
    
    for msg in messages:
        # Converter timestamp para datetime se necessário
        if isinstance(msg['timestamp'], str):
            timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
        else:
            timestamp = msg['timestamp']
        
        if timestamp.date() == today:
            messages_today.append(msg)
    
    if not messages_today:
        return []
    
    # Agrupar por sender
    sender_data = defaultdict(lambda: {'scores': [], 'count': 0})
    
    for msg in messages_today:
        sender = msg['sender']
        sender_data[sender]['scores'].append(msg['proba_resenha'])
        sender_data[sender]['count'] += 1
    
    # Calcular métricas
    ranking = []
    
    for sender, data in sender_data.items():
        I = np.mean(data['scores'])  # Mean score
        n = data['count']             # Message count
        V = 1 - np.exp(-n / VOLUME_FACTOR)  # Volume factor
        M = 0.7 * I + 0.3 * V        # Combined metric
        
        ranking.append({
            'sender': sender,
            'I': float(I),
            'n': int(n),
            'V': float(V),
            'M': float(M)
        })
    
    # Ordenar por M (descendente)
    ranking.sort(key=lambda x: x['M'], reverse=True)
    
    return ranking