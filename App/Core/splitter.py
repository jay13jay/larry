import json
import os

from Core import orc
from Schemas.schemas import ReturnMessageSchema

class Splitter:
    """
    A component that analyzes questions to determine their complexity and dimensionality.
    """
    
    def __init__(self, core):
        """
        Initialize the Splitter with a language model.
        
        Args:
            llm: The language model to use for analysis
        """
        self.llm = core.llm
    
    
    def analyze_question(self, question):
        """
        Analyze a question to determine its dimensions.
        
        Args:
            question (str): The question to analyze
            
        Returns:
            dict: Analysis results containing 'questions' and 'confidence'
        """
        prompt = f"""
        {orc.load_prompt("splitter")}
        
        Question:
        {question}
        
        Answer:
        """
        
        # Get raw response from the LLM
        response_str = self.llm.invoke(prompt)
        
        try:
            # Parse the JSON string into a Python dictionary
            dimensions = json.loads(response_str)
            return ReturnMessageSchema(
                status="success", 
                response=json.dumps({
                    "questions": dimensions["questions"],
                    "confidence": dimensions["confidence"]
                }),
                error=None
            ).model_dump()
            
        except json.JSONDecodeError:
            print("Failed to parse JSON from splitter response")
            return ReturnMessageSchema(
                status="failure",
                response=response_str,
                error="Failed to parse response"
            ).model_dump()