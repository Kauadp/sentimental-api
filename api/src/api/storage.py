import pandas as pd
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

def load_messages() -> pd.DataFrame:
    """Load messages from database."""
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
        return pd.DataFrame(data)
    finally:
        db.close()
