import os
import logging
import json
from jinja2 import Template
from transformers import pipeline
import torch

# Configure logging
logging.basicConfig(filename='logs/chat.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s [%(pathname)s:%(lineno)d]')
logging.info("Chat module loaded")

class Message:
    def __init__(self, text, role):
        """
        Initialize a Message instance.

        Args:
            text (str): The content of the message.
            role (str): The role of the message sender (e.g., 'USER', 'ASSISTANT').
        """
        self.text = text
        self.role = role

        self.format_message()

    def format_message(self):
        """
        Format the message using the Jinja2 template.

        Returns:
            str: The formatted message.
        """
        with open("tpl/chat.jinja2", 'r') as file:
            template_content = file.read()
        template = Template(template_content)
        return template.render(role=self.role, text=self.text)

    @classmethod
    def create_message(cls, text, role):
        """
        Create and format a new message.

        Args:
            text (str): The content of the message.
            role (str): The role of the message sender.

        Returns:
            str: The formatted message.
        """
        message = cls(text, role)
        return message.format_message()

class Chat:
    def __init__ (self, path="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """
        Initialize a Chat instance.

        Args:
            path (str): The path to the model.
        """
        self.path = path  # Path to the model
        self.pipe = pipeline("text-generation", model=path, torch_dtype=torch.bfloat16, device_map="auto")  # Text generation pipeline
        self.history = []  # List to store chat history
        self.template = self.load_template("tpl/chat.jinja2")  # Load the chat template
        self.history_file = "chat_history.txt"  # File to store chat history
        # Clear the history file at the start
        with open(self.history_file, 'w') as file:
            file.write("")

    def load_template(self, template_path):
        """
        Load a Jinja2 template from a file.

        Args:
            template_path (str): The path to the template file.

        Returns:
            Template: The loaded Jinja2 template.
        """
        with open(template_path, 'r') as file:
            template_content = file.read()
        return Template(template_content)
    
    def append_history(self, user_message, assistant_response):
        """
        Append user and assistant messages to the chat history.

        Args:
            user_message (str): The user's message.
            assistant_response (str): The assistant's response.
        """
        user_msg = Message.create_message(user_message, "USER")
        assistant_msg = Message.create_message(assistant_response, "ASSISTANT")
        self.history.append(Message(user_msg, "USER"))
        self.history.append(Message(assistant_msg, "ASSISTANT"))

    def new_message(self, text, menu):
        """
        Process a new message and generate a response.

        Args:
            text (str): The user's message.
            menu (dict): The menu options.
        """
        logging.info(f"New message received: {text}")
        # Prepare the history for the template
        history_text = "\n".join(message.text for message in self.history)
        # Render the template with the menu and history
        prompt = self.pipe.tokenizer.apply_chat_template(self.history, tokenize=False, add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        output = outputs[0]["generated_text"]
        logging.info(f"Model response: {output}")
        self.history.append(Message(output))
        # Append the new message and response to the history file
        with open(self.history_file, 'a') as file:
            file.write(f"USER: {text}\nASSISTANT: {output}\n")

    def load_menu(self, file_path):
        """
        Load the menu options from a JSON file.

        Args:
            file_path (str): The path to the menu file.

        Returns:
            dict: The loaded menu options.
        """
        with open(file_path, 'r') as file:
            menu = json.load(file)
        return menu
