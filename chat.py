import os
import logging
import json
from jinja2 import Template
from transformers import pipeline
import torch

# Configure logging
logging.basicConfig(filename='logs/chat.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s [%(pathname)s:%(lineno)d]')

# Set the logging level for the inotify logger to WARNING
logging.getLogger('inotify').setLevel(logging.WARNING)

class Message:
    def __init__ (self, text):
        self.text = text

class Chat:
    def __init__ (self, path="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.path = path
        self.pipe = pipeline("text-generation", model=path, torch_dtype=torch.bfloat16, device_map="auto")
        self.history = []
        self.template = self.load_template("tpl/chat.jinja2")
        self.history_file = "chat_history.txt"
        # Clear the history file at the start
        with open(self.history_file, 'w') as file:
            file.write("")

    def load_template(self, template_path):
        with open(template_path, 'r') as file:
            template_content = file.read()
        return Template(template_content)

    def new_message(self, text, menu):
        logging.debug(f"New message received: {text}")
        # Prepare the history for the template
        history_text = "\n".join(message.text for message in self.history)
        # Render the template with the menu and history
        prompt = self.template.render(menu="", history=history_text, input=text)
        outputs = self.pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        output = outputs[0]["generated_text"]
        print("Output: {}".format(output))
        logging.debug(f"Model response: {output}")
        self.history.append(Message(output))
        # Append the new message and response to the history file
        with open(self.history_file, 'a') as file:
            file.write(f"USER: {text}\nASSISTANT: {output}\n")

    def load_menu(self, file_path):
        with open(file_path, 'r') as file:
            menu = json.load(file)
        return menu
