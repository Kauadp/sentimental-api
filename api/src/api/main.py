from fastapi import FastAPI, HTTPException
from .models import MessageIn
from .storage import save_message_with_inference, load_messages
from .services.scoring import generate_alerts
from .services.ranking import generate_daily_ranking

app = FastAPI(title="Sentiment Analysis API")

@app.post("/message")
def receive_message(message: MessageIn):
    try:
        save_message_with_inference(message.model_dump())
        return {"status": "Message processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
def get_alerts():
    df = load_messages()
    return {"alerts": generate_alerts(df)}

@app.get("/ranking")
def get_ranking():
    df = load_messages()
    return {"ranking": generate_daily_ranking(df)}
