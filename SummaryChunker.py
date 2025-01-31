from PromptManager import *
from LLMProvider import *
from pydantic import BaseModel, Field

from typing import Tuple, List, Dict, Optional, Any
from langchain.schema import Document

class SummaryChunker:
    """
    A class for summarizing documents and combining the summaries with the original content.
    """

    class GenerateSummary(BaseModel):
        summary: str = Field(
            description="Summary of the document"
        )

    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.structured_llm = self.initialize_structured_llm()
        self.prompt_template = self.prompt_manager.get_prompt("summary_generation")

    def initialize_structured_llm(self):

        return self.llm_provider.get_llm().with_structured_output(self.GenerateSummary)

    def update_structured_llm(self):
        self.structured_llm = self.initialize_structured_llm()

    def generate_summaries(self, documents: List[Document]) -> List[Document]:

        processed_documents = []
        max_retries = len(self.llm_provider.api_keys)

        for i, doc in enumerate(documents):
            retries = 0
            while retries < max_retries:
                try:
                    prompt = self.prompt_template.format(text=doc.page_content)

                    response = self.structured_llm.invoke(prompt)

                    if response and response.summary:
                        summary = response.summary
                        new_content = f"الملخص : {summary}\n{doc.page_content}"

                        processed_doc = Document(
                            page_content=new_content,
                            metadata={"source": doc.metadata.get("source", ""), "chunk_id": i + 1}
                        )
                        processed_documents.append(processed_doc)

                        print(f"Original Content: {doc.page_content}")
                        print(f"Summary: {summary}")
                        print(f"Combined Content: {new_content}")
                        print("-" * 80)
                        break

                except Exception as e:
                    print(f"Error with API key {self.llm_provider.api_key_index}: {str(e)}")
                    retries += 1

                    if retries < max_retries:
                        print(f"Retrying with new API key (attempt {retries + 1}/{max_retries})")
                        self.llm_provider.switch_api_key()
                        self.update_structured_llm()
                    else:
                        print(f"Failed after {max_retries} attempts. Keeping original document.")
                        processed_documents.append(doc)

        return processed_documents
