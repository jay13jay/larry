import uuid
from datetime import datetime
from App.Schemas.schemas import MessageSchema, ReturnMessageSchema
from pydantic import ValidationError

class ChatSession:
    def __init__(self, user_name):
        self.chat_id = str(uuid.uuid4())
        self.user_name = user_name
        self.messages = []

    def add_message(self, text):
        try:
            message_data = MessageSchema(
                text=text,
                user=self.user_name,
                id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat()
            )
        except ValidationError as e:
            return ReturnMessageSchema(
                message=None,
                status='failure',
                error=str(e)
            ).model_dump(), 400
        
        self.messages.append(message_data)
        return ReturnMessageSchema(
            message=message_data,
            status='success',
            error=None
        ).model_dump()

    def get_messages(self):
        return [message.model_dump() for message in self.messages]
