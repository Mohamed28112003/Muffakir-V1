


from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *

from PromptManager import *


from RAGPipelineManager import RAGPipelineManager
from DocumentRetriever import *
from AnswerGenerator import *

class RAGGenerationPipeline:
    """Main class for handling the complete RAG generation pipeline"""

    def __init__(
        self,
        pipeline_manager: RAGPipelineManager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        k: int = 7
    ):
        self.retriever = DocumentRetriever(pipeline_manager)
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        self.k = k

    def generate_response(self, query: str) -> Dict[str, Any]:
        """
        Generate a response for a given query using the RAG pipeline

        Returns:
            Dict containing the generated answer and retrieval metadata
        """
        # Retrieve relevant documents
        retrieval_result = self.retriever.retrieve_documents(query, self.k)

        # Format documents
        formatted_documents = self.retriever.format_documents(retrieval_result)

        # Generate answer
        answer = self.generator.generate_answer(query, formatted_documents)

        return {
            "answer": answer,
            "retrieved_documents": [doc.page_content for doc in formatted_documents],
            "source_metadata": [doc.metadata for doc in formatted_documents],
        }