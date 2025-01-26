from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class DocGrader:
    def __init__(self, llm):
        self.prompt = PromptTemplate(
            template="""
            system
            You are a grader assessing relevance of a retrieved document to a user question. If the document contains keywords related to the user question, grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
            Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            user
            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {question} \n assistant""",
            input_variables=["question", "document"],
        )
        self.grader = self.prompt | llm | JsonOutputParser()

    def grade(self, question, document):
        return self.grader.invoke({"question": question, "document": document})