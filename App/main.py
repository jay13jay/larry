from flask import Flask, request, jsonify
# from Schemas.schemas import ReturnMessageSchema
from Chat.clerk import ChatSession

app = Flask(__name__)

# Initialize a chat session with a default user name
chat_session = ChatSession(user_name="client")

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = chat_session.get_messages()
    return jsonify({
        'status': "success",
        'response': {'messages': messages},
        'error': None
    })

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message_text = data.get('text')
    if not message_text:
        return jsonify({
            'status': "failure",
            'response': None,
            'error': 'No message text provided. Use "text" field.'
        }), 400
    
    response = chat_session.add_message(message_text)
    return jsonify({
        'status': "success",
        'response': response,
        'error': None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
