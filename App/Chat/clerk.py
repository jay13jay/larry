import uuid
from datetime import datetime
# from Schemas.schemas import MessageSchema, ReturnMessageSchema  # Remove these imports
from pydantic import ValidationError
from Core.orc import RAGCore
from components import vector_store, embedder, llm  # Add this import

class ChatSession:
    def __init__(self, user_name):
        self.chat_id = str(uuid.uuid4())
        self.user_name = user_name
        self.messages = []
        self.rag_core = RAGCore(vector_store, embedder, llm)  # Initialize RAGCore with appropriate arguments

    def add_message(self, text):
        try:
            # Remove MessageSchema usage
            message_data = {
                'text': text,
                'user': self.user_name,
                'id': uuid.uuid4(),  # Remove str() - provide actual UUID
                'timestamp': datetime.now()  # Remove isoformat() - provide actual datetime
            }
        except ValidationError as e:
            return {
                'message': None,
                'status': 'failure',
                'error': str(e),
                'response': []  # Ensure response is a list
            }, 400
        
        self.messages.append(message_data)
        
        # Call a function from orc after messages.append
        response = self.rag_core.new_user_query(question=text)
        
        return {
            'message': message_data,
            'status': 'success',
            'error': None,
            'response': [response]  # Ensure response is a list
        }

    def get_messages(self):
        return self.messages
