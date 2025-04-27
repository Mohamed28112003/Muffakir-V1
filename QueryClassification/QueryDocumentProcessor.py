from PromptManager.PromptManager import *
from LLMProvider.LLMProvider import *

class QueryDocumentProcessor:
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.query_classification_prompt = prompt_manager.get_prompt("query_classification_prompt")

    def classify_query(self, query: str) -> str:
        try:
            llm = self.llm_provider.get_llm()
            prompt = self.query_classification_prompt.format(query_transformed=query)
            response = llm.invoke(prompt)
            if hasattr(response, 'content'):
                print("classsss !!!! ", response.content)
                return response.content.strip()
            elif isinstance(response, str):
                return response.strip()
            else:
                return str(response).strip()
        except Exception as e:
            print(f"Error transforming query: {e}")
            print("Switching API key and retrying QUERY...")
            self.llm_provider.switch_api_key()
            return self.classify_query(query)

    def classify_query_with_history(self, conversation_history: str, new_query: str) -> str:

        try:
            llm = self.llm_provider.get_llm()
            history_prompt = self.prompt_manager.get_prompt("history_classification_prompt")
            prompt = history_prompt.format(conversation_history=conversation_history, new_query=new_query)
            response = llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content.strip()
            elif isinstance(response, str):
                return response.strip()
            else:
                return str(response).strip()
        except Exception as e:
            print(f"Error classifying query with history: {e}")
            self.llm_provider.switch_api_key()
            return self.classify_query_with_history(conversation_history, new_query)


