from typing import List, Union
import logging

from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
from langchain.schema import Document



class MindMap:
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.logger = logging.getLogger(__name__)
        self.mindmap_prompt = self.prompt_manager.get_prompt("mindmap")

    def generate_mindmap(
        self,
        documents: Union[List[Document], str]
    ) -> str:
        if isinstance(documents, str):
            context = documents
        else:
            try:
                context = "\n\n".join(doc.page_content for doc in documents)
            except Exception as e:
                self.logger.error(f"Failed to join page_content: {e}", exc_info=True)
                context = str(documents)

        try:
            prompt = self.mindmap_prompt.format(
                context=context,

            )
        except Exception as e:
            self.logger.error(f"Failed to format mindmap prompt: {e}", exc_info=True)
            prompt = f"Context:\n{context}\n\nMindmap:"

        try:
            llm = self.llm_provider.get_llm()
            if hasattr(llm, "invoke"):
                response = llm.invoke(prompt)
            else:
                response = llm(prompt)

            if hasattr(response, "content"):
                return response.content
            return str(response)

        except Exception as e:
            self.logger.error(f"Error generating mindmap from LLM: {e}", exc_info=True)
            return "mindmap generation failed."
