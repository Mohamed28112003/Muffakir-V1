
from LLMProvider.LLMProvider import *
from PromptManager.PromptManager import *

class LLMJudge:

    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.llm_judge_prompt = prompt_manager.get_prompt("rag_evaluation_prompt")

    def check_answer_relevance(self, ground_truth: str,system_answer:str) -> str:

        try:
            llm = self.llm_provider.get_llm()
            prompt = self.llm_judge_prompt.format(ground_truth=ground_truth,system_answer=system_answer)
            response = llm.invoke(prompt)

            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            print(f"Error LLM Judge: {e}")
            