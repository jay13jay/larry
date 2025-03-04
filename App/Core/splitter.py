import json
import os

class Splitter:
    """
    A class to handle splitting multi-faceted questions into sub-questions.
    Methods:
        split_question(question):
            Splits the given question into sub-questions and returns the result as a JSON string.
    """

    def __init__(self, llm, prompt_loader):
        """
        Initialize with a prompt loader and llm.
        """
        self.llm = llm
        self.prompt_text = prompt_loader("splitter")


    def split_question(self, question):
        '''Splits the given question into sub-questions'''
        prompt = f"""
        {self.prompt_text}
        
        Question:
        {question}
        """
        response = self.llm.invoke(prompt)
        return response