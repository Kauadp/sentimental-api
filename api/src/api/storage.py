from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, Message
from .services.inference import infer_probability

def save_message_with_inference(message: dict):
    """Save message with sentiment inference to database."""
    db: Session = SessionLocal()
    try:
        # Add inference
        message_dict = message.copy()
        message_dict['proba_resenha'] = infer_probability(message_dict['message'])
        
        # Create Message object
        db_message = Message(
            group_id=message_dict['group_id'],
            sender=message_dict['sender'],
            message=message_dict['message'],
            proba_resenha=message_dict['proba_resenha'],
            timestamp=message_dict['timestamp']
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
    finally:
        db.close()

def load_messages() -> List[Dict]:
    """Load messages from database as list of dictionaries."""
    db: Session = SessionLocal()
    try:
        messages = db.query(Message).all()
        data = [{
            'group_id': msg.group_id,
            'sender': msg.sender,
            'message': msg.message,
            'proba_resenha': msg.proba_resenha,
            'timestamp': msg.timestamp
        } for msg in messages]
        return data
    finally:
        db.close()

def load_messages_dict() -> Dict[str, List]:
    """Load messages from database in pandas-compatible dict format.
    
    Returns dict with column names as keys and lists of values.
    Useful if you need to maintain compatibility with code expecting DataFrame structure.
    """
    messages = load_messages()
    
    if not messages:
        return {
            'group_id': [],
            'sender': [],
            'message': [],
            'proba_resenha': [],
            'timestamp': []
        }
    
    return {
        'group_id': [msg['group_id'] for msg in messages],
        'sender': [msg['sender'] for msg in messages],
        'message': [msg['message'] for msg in messages],
        'proba_resenha': [msg['proba_resenha'] for msg in messages],
        'timestamp': [msg['timestamp'] for msg in messages]
    }