from typing import List, Dict, Any ,Optional
from langchain.schema import Document
from RAGPipelineManager import *

class DocumentRetriever:
    def __init__(self, pipeline_manager: Optional[RAGPipelineManager]=Any):
        self.pipeline_manager = pipeline_manager

    def retrieve_documents(self, query: str, k: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves top-k similar documents and extracts source & page_content.
        Returns a list of dictionaries containing:
        - "source": the source of the document
        - "page_content": the content of the document
        """
        results = self.pipeline_manager.query_similar_documents(query, k)  

        retrieved_data = [
            {
                "source": doc.metadata.get("source", "Unknown"),  
                "page_content": doc.page_content  
            }
            for doc in results 
        ]

        return retrieved_data

    def format_documents(self, retrieval_result: List[Dict[str, Any]]) -> List[Document]:
        """
        Formats the retrieved data into LangChain's Document objects.
        """
        return [
            Document(page_content=item["page_content"], metadata={"source": item["source"]})
            for item in retrieval_result
        ]
