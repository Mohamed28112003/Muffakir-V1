from typing import Dict,Any
from enum import Enum
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
from Generation.AnswerGenerator import AnswerGenerator
from QueryClassification.QueryDocumentProcessor import QueryDocumentProcessor
from HallucinationsCheck.HallucinationsCheck import HallucinationsCheck
from WebSearch.Search import Search
from QueryTransformer.QueryTransformer import QueryTransformer
from Enums import QueryType


class RAGGenerationPipeline:
    
    def __init__(
        self,
        pipeline_manager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        query_processor: QueryDocumentProcessor,
        hallucination: HallucinationsCheck,
        k: int = 5
    ):
        self.pipeline_manager = pipeline_manager
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.query_processor = query_processor
        self.hallucination = hallucination
        
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        self.query_transformer = QueryTransformer(llm_provider, prompt_manager, prompt="search_query")
        self.k = k
        
    def _process_dummy_query(self, query: str) -> Dict[str, Any]:
        llm = self.llm_provider.get_llm()
        response = llm.invoke(query)
        
        if hasattr(response, 'content'):
            answer = self.hallucination.check_answer(response.content)
        else:
            answer = self.hallucination.check_answer(str(response))
        
        return {
            "answer": answer,
            "retrieved_documents": [],
            "source_metadata": [],
        }
        
    def _process_vector_db_query(self, query: str) -> Dict[str, Any]:
        from Generation.DocumentRetriever import DocumentRetriever

        retriever = DocumentRetriever(self.pipeline_manager )
        retrieval_result = retriever.retrieve_documents(query, self.k)
        formatted_documents = retriever.format_documents(retrieval_result)
        
        answer = self.generator.generate_answer(query, formatted_documents)
        
        if answer in "لا يمكنني الإجابة على هذا السؤال":
            return self._perform_web_search_fallback(query)
        
        
        return {
            "answer": answer,
            "retrieved_documents": [doc.page_content for doc in formatted_documents],
            "source_metadata": [doc.metadata for doc in formatted_documents],
        }
        
    def _perform_web_search_fallback(self, query: str) -> Dict[str, Any]:
        optimized_query = self.query_transformer.transform_query(query)
        
        search_instance = Search(
            api_key=self._get_search_api_key(),
            llm_provider=self.llm_provider,
            prompt_manager=self.prompt_manager,
            params=self._get_search_params()
        )
        
        results = search_instance.deep_search(optimized_query)
        final_analysis = results["data"].get("finalAnalysis", "لا يوجد تحليل متاح.")
        sources = results["data"].get("sources", [])


        
        return {
            "answer": final_analysis,
            "retrieved_documents": [],
            "source_metadata": sources,
        }
    
    def _get_search_api_key(self) -> str:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("FIRE_CRAWL_API")
    
    def _get_search_params(self) -> Dict[str, Any]:
        return {
            "maxDepth": 3,
            "timeLimit": 30,
            "maxUrls": 5
        }
    
    def generate_response(self, query: str) -> Dict[str, Any]:
        """Main entry point to generate a response"""
        query_type = self.query_processor.classify_query(query=query)
        
        if query_type == QueryType.DUMMY_QUERY.value:
            return self._process_dummy_query(query)
        elif query_type == QueryType.VECTOR_DB.value:
            return self._process_vector_db_query(query)
        else:
            raise ValueError(f"Unknown query type: {query_type}")