


from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *

from PromptManager import *

from Reranker import *  
from RAGPipelineManager import RAGPipelineManager
from DocumentRetriever import *
from AnswerGenerator import *



class RAGGenerationPipeline:
    """Main class for handling the complete RAG generation pipeline with reranking"""

    def __init__(
        self,
        pipeline_manager: RAGPipelineManager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        reranker: Optional[Reranker] = None,
        k: int = 7
    ):
        self.retriever = DocumentRetriever(pipeline_manager)
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        self.reranker = reranker or Reranker()  # Default reranker if not provided
        self.k = k

    def generate_response(self, query: str) -> Dict[str, Any]:
        """
        Generate a response for a given query using the RAG pipeline with optional reranking

        Returns:
            Dict containing the generated answer and retrieval metadata
        """

        
        # Retrieve relevant documents
        retrieval_result = self.retriever.retrieve_documents(query, self.k)

        # Format documents
        formatted_documents = self.retriever.format_documents(retrieval_result)

        # Rerank documents
        reranked_documents = self.reranker.rerank(query, formatted_documents)

        # Generate answer using reranked documents
        answer = self.generator.generate_answer(query, reranked_documents)

        return {
            "answer": answer,
            "retrieved_documents": [doc.page_content for doc in reranked_documents],
            "source_metadata": [doc.metadata for doc in reranked_documents],
        }