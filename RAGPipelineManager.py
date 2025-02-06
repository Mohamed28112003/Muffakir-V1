
from typing import Tuple, List, Dict, Optional, Any
from QueryTransformer import *
from LLMProvider import *
from langchain.schema import Document

from PromptManager import *

from ChromaDBManager import *
from RetrieveMethods import  *

from Reranker import *

class RAGPipelineManager:
    """
    A manager class for the RAG (Retrieval-Augmented Generation) pipeline.
    """
    def __init__(
        self,
        db_path: str,
        collection_name: str = 'Book',
        model_name: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        query_transformer: QueryTransformer = None,
        llm_provider: Optional[LLMProvider] = None,
        prompt_manager: Optional[PromptManager] = None,
        k: int = 2 ,
        fetch_k: int = 7,
        retrive_method: str = "max_marginal_relevance_search",
         reranker: Optional[Reranker] = None,
    ):

        self.db_manager = ChromaDBManager(
            path=db_path,
            collection_name=collection_name,
            model_name=model_name
        )
        from RAGGenerationPipeline import RAGGenerationPipeline

        self.query_transformer = query_transformer
        
        self.generation_pipeline = RAGGenerationPipeline(
            pipeline_manager=self,
            llm_provider=llm_provider,
            prompt_manager=prompt_manager,
            reranker=reranker
        )
        self.k = k
        self.fetch_k = fetch_k
        self.retrive_method = retrive_method
        self.retriever = RetrieveMethods(self.db_manager.vector_store)
        self.llm_provider = llm_provider
        self.reranker = reranker




    def store_documents(self, documents: List[Document]):
        self.db_manager.add_documents(documents)

    def query_similar_documents(self, query: str, k: Optional[int] = None) -> Dict[str, Any]:
        ## Optional
        #query = self.query_transformer.transform_query(query)
        ## class = query_classfication(query)

        ## dummy llm
        ## vb 
        ## (agent)
 
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
        return self.generation_pipeline.generate_response(query)


