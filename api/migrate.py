import pandas as pd
from sqlalchemy.orm import Session
from src.api.database import SessionLocal, Message, engine, Base
from src.api.config import MESSAGES_FILE

# Create tables
Base.metadata.create_all(bind=engine)

# Load existing data
if MESSAGES_FILE.exists():
    df = pd.read_json(MESSAGES_FILE, lines=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format='mixed', utc=True)
    
    db: Session = SessionLocal()
    try:
        for _, row in df.iterrows():
            db_message = Message(
                group_id=row.get('group_id', ''),
                sender=row['sender'],
                message=row['message'],
                proba_resenha=row['proba_resenha'],
                timestamp=row['timestamp']
            )
            db.add(db_message)
        db.commit()
        print("Migração concluída!")
    except Exception as e:
        print(f"Erro na migração: {e}")
        db.rollback()
    finally:
        db.close()
else:
    print("Arquivo messages.jsonl não encontrado, pulando migração.")