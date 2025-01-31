from LLMProvider import *
from PromptManager import *

class QueryGenerator:
    """
    A class responsible for generating queries from text chunks.
    """
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.query_prompt_template = self.prompt_manager.get_prompt("question_generation")

    def generate_query(self, chunk_text: str) -> str:

        try:
            prompt = self.query_prompt_template.format(text=chunk_text)

            llm = self.llm_provider.get_llm()
            response = llm.invoke(prompt)

            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)

        except Exception as e:
            print(f"Error generating query: {e}")
            print("Switching API key and retrying...")
            self.llm_provider.switch_api_key()
            return self.generate_query(chunk_text)
