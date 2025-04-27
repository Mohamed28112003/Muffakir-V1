
from QueryTransformer.QueryTransformer import *
from LLMProvider.LLMProvider import *
from langchain.schema import Document

from PromptManager.PromptManager import *

from VectorDB.ChromaDBManager import *
from RAGPipeline.RetrieveMethods import  *

from QueryClassification.QueryDocumentProcessor import *

from Reranker.Reranker import *
from HallucinationsCheck.HallucinationsCheck import *
from typing import  List, Dict, Optional, Any

from langchain.schema import Document


class RAGPipelineManager:
    def __init__(
        self,
        db_path: str,
        collection_name: str = 'Book',
        model_name: str = 'mohamed2811/Muffakir_Embedding',
        query_transformer: QueryTransformer = None,
        llm_provider: Optional[LLMProvider] = None,
        prompt_manager: Optional[PromptManager] = None,
        k: int = 2,
        fetch_k: int = 7,
        retrive_method: str = "max_marginal_relevance_search",
        reranker: Optional[Reranker] = None,
        query_processor: Optional[QueryDocumentProcessor] = None,
        hallucination: Optional[HallucinationsCheck] = None,
       
    ):
        self.db_manager = ChromaDBManager(
            path=db_path,
            collection_name=collection_name,
            model_name=model_name
        )


        # NEW

        self.query_transformer = query_transformer

        from Generation.RAGGenerationPipeline import RAGGenerationPipeline
        self.generation_pipeline = RAGGenerationPipeline(
            pipeline_manager=self,
            llm_provider=llm_provider,
            prompt_manager=prompt_manager,
            reranker=reranker,
            
            hallucination=hallucination,
            query_processor=query_processor
        )
        self.k = k
        self.fetch_k = fetch_k
        self.retrive_method = retrive_method
        self.retriever = RetrieveMethods(self.db_manager.vector_store)
        self.llm_provider = llm_provider
        self.reranker = reranker
        self.db_path = db_path
        self.query_transformer =query_transformer




    def store_documents(self, documents: List[Document]):
        self.db_manager.add_documents(documents)

    def query_similar_documents(self, query: str, k: Optional[int] = None) -> Dict[str, Any]:


        if self.retrive_method == "max_marginal_relevance_search":
            return self.retriever.max_marginal_relevance_search(query,self.k,self.fetch_k)


        elif self.retrive_method == "similarity_search":
            return self.retriever.similarity_search(query, self.k)

        elif self.retrive_method=="hybrid":
            return self.retriever.HybridRAG(query,self.k)

        elif self.retrive_method =="contextual":

            return self.retriever.ContextualRAG(llm_provider= self.llm_provider,query=query)

        else:
            raise ValueError(f"Unknown retrive_method: {self.retrive_method}")


    def generate_answer(self, query: str) -> Dict[str, Any]:

        ## query transformer 
        #query = self.query_transformer.transform_query(query)


        return self.generation_pipeline.generate_response(query,type=self.retrive_method)


