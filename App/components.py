import os
import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma

# Create an absolute path for the vector store
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector_db")
print(f"Using vector database at: {VECTOR_DB_PATH}")

# Create directory for vector store if it doesn't exist
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# Initialize the embedder using Ollama with an embedding model
embedder = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)

# Initialize vector store using ChromaDB with absolute path
persistent_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = persistent_client.get_or_create_collection("knowledge_base")

vector_store = Chroma(
    client=persistent_client,
    collection_name="knowledge_base",
    embedding_function=embedder
)

# Initialize LLM using Ollama
llm = OllamaLLM(
    # model="granite",
    model="granite3.1-dense:8b",
    base_url="http://localhost:11434",
    temperature=0.1
)