from langchain_community.chat_models import ChatOllama

from langgraph.graph import END, StateGraph, START
from typing import TypedDict, List
from dotenv import load_dotenv

from router.router import Router
from tools.search import Search
from tools.docFetch import DocFetch
from tools.docGrader import DocGrader
from tools.generate import Generator

# Load environment variables from .env file
load_dotenv()

llm = ChatOllama(model="llama3", format="json", temperature=0.0)
search = Search().search
retrieve = DocFetch().retrieve
grader =  DocGrader(llm).grade
generate = Generator(llm).generate
router = Router(llm)
# tools = [search]


class GraphState(TypedDict):
    question: str
    generation: str
    web_search: str
    documents: List[str]

def decide_to_generate(state: GraphState) -> str:
    # Logic to decide whether to generate based on graded documents
    if state['documents']:
        return "generate"
    return "websearch"

def grade_generation_v_documents_and_question(state: GraphState) -> str:
    # Logic to grade the generation versus documents and question
    if state['generation'] in state['documents']:
        return "useful"
    return "not useful"


workflow = StateGraph(GraphState)

workflow.add_node("websearch", search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grader)
workflow.add_node("generate", generate)

workflow.add_conditional_edges(
    START,
    router.route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)

workflow.add_edge("retrieve", "grade_documents")

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
    },
)

app = workflow.compile()