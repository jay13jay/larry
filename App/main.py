from flask import Flask, request, jsonify
from Schemas.schemas import ReturnMessageSchema
from Chat.clerk import ChatSession

app = Flask(__name__)

# Initialize a chat session with a default user name
chat_session = ChatSession(user_name="client")

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = chat_session.get_messages()
    return jsonify({'messages': messages})  # Just return the list directly

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message_text = data.get('text')
    if not message_text:
        return jsonify({'error': 'No message text provided. Use "text" field.'}), 400
    
    response = chat_session.add_message(message_text)
    # response is already a dict from model_dump() in clerk.py
    return jsonify(response)  # Just return the response directly

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
