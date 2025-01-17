import logging
from flask import Flask, request, jsonify
from chat import Chat

# Configure logging
logging.basicConfig(filename='logs/chat.log', level=logging.ERROR, 
                    format='%(asctime)s %(levellevel)s %(message)s [%(pathname)s:%(lineno)d]')

app = Flask(__name__)

# Initialize the chat model
chat = Chat()
menu = chat.load_menu('files/pino_menu.json')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({"error": "No message provided"}), 400

    logging.debug(f"Received message: {message}")
    chat.new_message(message, menu)
    response = chat.history[-1].text  # Ensure the last message is the assistant's response
    logging.debug(f"Response: {response}")
    return jsonify({"response": response})

@app.route('/get_history', methods=['GET'])
def get_history():
    history = []
    for i in range(0, len(chat.history), 2):
        user_message = chat.history[i].text
        assistant_response = chat.history[i + 1].text if i + 1 < len(chat.history) else ""
        history.append({"user": user_message, "assistant": assistant_response})
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
