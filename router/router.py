from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class Router:
    def __init__(self, llm):
        self.template = PromptTemplate(
            template="""
    system You are an expert at routing a user question to a vectorstore or web search.
    Use the vectorstore for questions on LLM agents, prompt engineering, and adversarial attacks.
    You do not need to be stringent with the keywords in the question related to these topics.
    Otherwise, use web-search. 
    Give a binary choice 'web_search' or 'vectorstore' based on the question.
    Return the a JSON with a single key 'datasource' and no preamble or explanation.
    Question to route: {question} assistant""",
            input_variables=["question"]
        )
        self.llm = llm
        self.question_router = self.template | self.llm | JsonOutputParser()

    def route_question(self, question):
        return self.question_router.invoke({"question": question})