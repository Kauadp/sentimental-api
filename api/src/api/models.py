from pydantic import BaseModel
from datetime import datetime

class MessageIn(BaseModel):
    group_id: str
    sender: str
    message: str
    timestamp: datetime
