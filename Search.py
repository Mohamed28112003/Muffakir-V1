from LLMProvider import *
from PromptManager import *
from firecrawl import FirecrawlApp
from QueryTransformer import *

class Search:

    def __init__(self, api_key: str, llm_provider: LLMProvider, prompt_manager: PromptManager, params: dict):
        self.firecrawl = FirecrawlApp(api_key=api_key)
        self.query_transformer = QueryTransformer(llm_provider, prompt_manager,prompt="search_query")
        self.params = params

    def deep_search(self, original_query: str, on_activity=None):
        optimized_query = self.query_transformer.transform_query(original_query)
        print(f"Optimized Query: {optimized_query}")
        results = self.firecrawl.deep_research(
            query=optimized_query,
            params=self.params,
            on_activity=on_activity
        )
        return results

