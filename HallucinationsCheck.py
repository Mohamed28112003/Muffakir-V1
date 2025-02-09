
from LLMProvider import *
from PromptManager import *

class HallucinationsCheck:
 
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.hallucination_check_prompt = prompt_manager.get_prompt("hallucination_check_prompt")

    def check_answer(self, answer: str) -> str:

        try:
            llm = self.llm_provider.get_llm()
            prompt = self.hallucination_check_prompt.format(answer=answer) ## propt
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
            return self.transform_query(answer)
