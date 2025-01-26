from langchain_community.tools.tavily_search import TavilySearchResults


class Search:
    def __init__(self):
        self.max_results = 2
        self.search_results = []
        self.search = TavilySearchResults(max_results=self.max_results)

    def invoke(self, query):
        results = self.search.invoke(query)
        return results