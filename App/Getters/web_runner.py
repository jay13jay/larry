from components import llm_vector_store, audio_gen_vector_store, embedder
from agent_dingo.rag.readers.web import WebpageReader
from agent_dingo.rag.chunkers.recursive import RecursiveChunker

# Read the content of the websites
reader = WebpageReader()
phi_3_docs = reader.read("https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/")
llama_3_docs = reader.read("https://ai.meta.com/blog/meta-llama-3/")
openvoice_docs = reader.read("https://research.myshell.ai/open-voice")

# Chunk the documents
chunker = RecursiveChunker(chunk_size=512)
phi_3_chunks = chunker.chunk(phi_3_docs)
llama_3_chunks = chunker.chunk(llama_3_docs)
openvoice_chunks = chunker.chunk(openvoice_docs)

# Embed the chunks
for doc in [phi_3_chunks, llama_3_chunks, openvoice_chunks]:
    embedder.embed_chunks(doc)

# Populate LLM vector store with embedded chunks about Phi-3 and Llama 3
for chunk in [phi_3_chunks, llama_3_chunks]:
    llm_vector_store.upsert_chunks(chunk)

# Populate audio gen vector store with embedded chunks about OpenVoice
audio_gen_vector_store.upsert_chunks(openvoice_chunks)