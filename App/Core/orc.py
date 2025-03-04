class RAGCore:
    def __init__(self, vector_store, embedder, llm):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm
        
    def query(self, user_question, top_k=5):
        # Convert question to embedding
        query_embedding = self.embedder.embed_query(user_question)
        
        # Retrieve relevant documents
        context_chunks = self.vector_store.search(query_embedding, top_k)
        
        # Format context for the LLM
        context_text = "\n\n".join([chunk.text for chunk in context_chunks])
        
        # Generate response with context
        prompt = f"""Answer the question based on the following context:
        
        Context:
        {context_text}
        
        Question: {user_question}
        
        Answer:"""
        
        return self.llm.generate(prompt)
