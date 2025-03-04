from flask import Flask, request, jsonify
from pydantic import ValidationError
from schemas import MessageSchema
import datetime
import uuid

app = Flask(__name__)

class ChatAPI:
    def __init__(self):
        self.messages = []

    def get_messages(self):
        # Return all message fields, not just text
        messages = [message.model_dump() for message in self.messages]
        return jsonify({'messages': messages})

    def send_message(self, data):
        # Extract just the message text from the request
        try:
            message_text = data.get('text')
            if not message_text:
                # Try to find the message in a different field if 'text' isn't provided
                message_text = data.get('message')
                
            if not message_text:
                return jsonify({'error': 'No message text provided. Use "text" field.'}), 400
            
            # Create a complete message with all required fields
            message_data = MessageSchema(
                text=message_text,
                user="client",
                id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now()
            )
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
        self.messages.append(message_data)
        
        # Return the full message object
        return jsonify({
            'message': message_data.model_dump(),
            'status': 'success'
        })

chat_api = ChatAPI()

@app.route('/messages', methods=['GET'])
def get_messages():
    return chat_api.get_messages()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    return chat_api.send_message(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
