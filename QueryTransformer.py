
from LLMProvider import *
from PromptManager import *

class QueryTransformer:
    """
    A class responsible for transforming queries to improve retrieval.
    """
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.query_rewrite_prompt = prompt_manager.get_prompt("query_rewrite")

    def transform_query(self, original_query: str) -> str:

        try:
            llm = self.llm_provider.get_llm()
            prompt = self.query_rewrite_prompt.format(original_query=original_query)
            response = llm.invoke(prompt)

            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            print(f"Error transforming query: {e}")
            print("Switching API key and retrying QUERY...")
            self.llm_provider.switch_api_key()
            return self.transform_query(original_query)
