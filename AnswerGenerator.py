
from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *
from langchain.schema import Document

from PromptManager import *


class AnswerGenerator:
    """Class for generating answers from retrieved documents"""

    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.generation_prompt = self.prompt_manager.get_prompt("generation")

    def generate_answer(self, query: str, documents: List[Document]) -> str:

        context = "\n\n".join([doc.page_content for doc in documents])

        try:
            prompt = self.generation_prompt.format(
                context=context,
                question=query
            )

            llm = self.llm_provider.get_llm()
            response = llm.invoke(prompt)

            if hasattr(response, 'content'):
                return response.content
            return str(response)

        except Exception as e:
            print(f"Error generating answer: {e}")
            self.llm_provider.switch_api_key()
            return self.generate_answer(query, documents)