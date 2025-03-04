from pydantic import BaseModel
import datetime
import uuid

class MessageSchema(BaseModel):
    text: str
    user: str
    id: uuid.UUID
    timestamp: datetime.datetime


class ReturnMessageSchema(BaseModel):
    message: MessageSchema
    status: str
    error: str