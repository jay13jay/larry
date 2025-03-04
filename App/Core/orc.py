import os
import json

class RAGCore:
    """
    A class to handle retrieval-augmented generation (RAG) using a vector store, an embedder, and a language model (LLM).
    This class is responsible for processing user questions, retrieving relevant documents, and generating responses.
    This class is meant to be used an an orchestrator, delegating tasks to other agents.
    Attributes:
        vector_store: An object that handles storage and retrieval of document embeddings.
        embedder: An object that converts text queries into embeddings.
        llm: A language model object that generates responses based on provided context.
    Methods:
        __init__(vector_store, embedder, llm):
            Initializes the RAGCore with a vector store, an embedder, and a language model.
        query(user_question, top_k=5):
            Processes a user question to generate a response using the vector store and language model.
            Args:
                user_question (str): The question asked by the user.
                top_k (int, optional): The number of top relevant documents to retrieve. Defaults to 5.
            Returns:
                str: The generated response from the language model.
    """

    def __init__(self, vector_store, embedder, llm):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm
        self.prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')


    def get_context(self, user_question, top_k=5):
        '''Convert question to embedding and get context from vector store'''

        # Convert question to embedding
        query_embedding = self.embedder.embed_query(user_question)
        
        # Retrieve relevant documents - FIXED: use named parameters and specify search_type
        context_chunks = self.vector_store.similarity_search_by_vector(
            embedding=query_embedding, 
            k=top_k
        )
        
        # Format context for the LLM
        context_text = "\n\n".join([chunk.page_content for chunk in context_chunks])

        return context_text

    def load_prompt(self, agent):
        '''Load the appropriate prompt based on provided agent name'''
        prompt_file = os.path.join(self.prompts_dir, f"{agent}.txt")
        if not os.path.exists(prompt_file):
            raise ValueError(f"Prompt for agent '{agent}' does not exist.")
        with open(prompt_file, 'r') as file:
            return file.read().strip()
        
    def query(self, question, agent, context_level):
        '''Generate response from agent to question with context'''        
        # Process regular query
        context = ""
        if context_level == 0:
            context = "NO CONTEXT"
        else:
            context = self.get_context(question, context_level)

        prompt= f"""
        {self.load_prompt(agent)}
    
        Context:
        {context}
        
        Question:
        {question}
        
        Answer:"""
        
        
        return self.llm.invoke(prompt)
    

    def new_user_query(self, question):
        '''Process a new user query'''
        # Determine if this is a multi-faceted question
        # If so, split into sub-questions
        q_dimensions_str = self.query(question, 'splitter', 0)
        print("Question dimensions:", q_dimensions_str)
        
        try:
            # Parse the JSON string into a Python dictionary
            q_dimensions = json.loads(q_dimensions_str)
            num_questions = q_dimensions["questions"]  # Remove the [0] indexing
            confidence = q_dimensions["confidence"]
            
            print(f"Number of questions: {num_questions} (Confidence: {confidence}%)")
            
            return f"Your question has {num_questions} parts with {confidence}% confidence."
            
        except json.JSONDecodeError:
            print("Failed to parse JSON from splitter response")
            return "I couldn't properly analyze your question. Please try again."
