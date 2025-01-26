from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class Generator:
    def __init__(self, llm):
        self.prompt = PromptTemplate(
            template="""system You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. user
            Question: {question}
            Context: {context}
            Answer: assistant""",
            input_variables=["question", "context"],
        )
        self.generator = self.prompt | llm | JsonOutputParser()

    def generate(self, question, context):
        return self.generator.invoke({"question": question, "context": context})