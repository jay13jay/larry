from pydantic import BaseModel
import datetime
import uuid
from typing import Optional, List

class MessageSchema(BaseModel):
    text: str
    user: str
    id: uuid.UUID
    timestamp: datetime.datetime

class ReturnMessageSchema(BaseModel):
    message: Optional[MessageSchema] = None
    status: str
    error: Optional[str] = None
    response: List = []