# Import relevant functionality
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def main():
    # Create the agent
    memory = MemorySaver()
    model = ChatOllama(
        model="llama3.1",
        temperature=0,
        # other params...
    )
    search = TavilySearchResults(max_results=2)
    tools = [search]
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    # Use the agent
    config = {"configurable": {"thread_id": "abc123"}}
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
    ):
        print(chunk)
        print("----")

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
    ):
        print(chunk['response'])
        print("----")

if __name__ == "__main__":
    main()