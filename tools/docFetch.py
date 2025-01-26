from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings

# Load environment variables from .env file
load_dotenv()

class DocFetch:
    def __init__(self):
        self.urls = [
            "https://pinosrva.com/order-online",
            # "https://example.com/post2",
            # "https://example.com/post3",
        ]
        self.docs = [WebBaseLoader(url).load() for url in self.urls]
        self.docs_list = [item for sublist in self.docs for item in sublist]
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
        self.doc_splits = self.text_splitter.split_documents(self.docs_list)
        self.vectorstore = Chroma.from_documents(
            documents=self.doc_splits,
            collection_name="rag-chroma",
            embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local"),
        )
        self.retrieve = self.vectorstore.as_retriever()