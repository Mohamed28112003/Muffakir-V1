from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field, ConfigDict
from langchain.schema import Document
from ChromaDBManager import ChromaDBManager

class DocumentSearchToolInput(BaseModel):
    """Input schema for DocumentSearchTool."""
    query: str = Field(..., description="Query to search the document.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Search the document for the given query."
    args_schema: Type[BaseModel] = DocumentSearchToolInput
    model_config = ConfigDict(extra="allow")
    
    def __init__(self, db_path: str, k: int = 5):
        """
        Initialize the searcher with ChromaDBManager.
        
        :param db_path: Path to the database.
        :param k: Number of document chunks to retrieve.
        """
        super().__init__()
        self.db_manager = ChromaDBManager(path=db_path)
        self.k = k  
        self._last_retrieved_docs = []
    
    def _run(self, query: str) -> str:
        """
        Search the document using ChromaDBManager.
        Returns a formatted string for the agent while storing the raw documents.
        
        :param query: The search query.
        :return: A string containing the formatted content of the retrieved chunks.
        """
        # Use the dynamic k parameter here
        relevant_chunks = self.db_manager.similarity_search(query, k=self.k)
        if not relevant_chunks:
            self._last_retrieved_docs = []
            return "لم يتم العثور على نتائج مطابقة في قاعدة البيانات."
        
        self._last_retrieved_docs = relevant_chunks
        
        docs = [chunk.page_content for chunk in relevant_chunks]
        separator = "\n___\n"
        return separator.join(docs)
    
    def get_last_retrieved_docs(self) -> List[Document]:
        """Return the documents retrieved from the last search."""
        return self._last_retrieved_docs
