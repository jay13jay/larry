class Researcher:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools  # Dictionary of tool_name: tool_function
        self.memory = []
        
    def think(self, user_input):
        # Format memory and available tools
        memory_str = "\n".join([f"{m['role']}: {m['content']}" for m in self.memory])
        tools_str = "\n".join([f"- {name}: {tool.__doc__}" for name, tool in self.tools.items()])
        
        # Planning prompt
        planning_prompt = f"""
        User input: {user_input}
        
        Previous conversation:
        {memory_str}
        
        Available tools:
        {tools_str}
        
        First, determine if you need to use any tools to answer this question.
        If yes, explain your reasoning and specify which tool to use with what parameters.
        If no, explain why the question can be answered directly.
        
        Reasoning:"""
        
        plan = self.llm.generate(planning_prompt)
        return self._execute_plan(plan, user_input)
    
    def _execute_plan(self, plan, user_input):
        # Extract tool calls or direct response based on plan
        # Execute tools if needed
        # Format final response
        # Update memory
        pass