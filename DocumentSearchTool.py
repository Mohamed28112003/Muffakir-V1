from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field, ConfigDict
from langchain.schema import Document
from ChromaDBManager import ChromaDBManager

class DocumentSearchToolInput(BaseModel):
    """مخطط الإدخال لأداة البحث في الوثائق."""
    query: str = Field(..., description="استعلام للبحث في الوثيقة.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "البحث في الوثيقة باستخدام الاستعلام المعطى."
    args_schema: Type[BaseModel] = DocumentSearchToolInput
    model_config = ConfigDict(extra="allow")
    
    def __init__(self, db_path: str, k: int = 5):
        """
        تهيئة الباحث باستخدام ChromaDBManager.
        
        :param db_path: مسار قاعدة البيانات.
        :param k: عدد أجزاء الوثيقة المراد استرجاعها.
        """
        super().__init__()
        self.db_manager = ChromaDBManager(path=db_path)
        self.k = k  
        self._last_retrieved_docs: List[Document] = []
    
    def _run(self, query: str) -> List[Document]:
        """
        البحث في الوثيقة باستخدام ChromaDBManager.
        يُعيد قائمة من كائنات Document المُسترجعة.
        
        :param query: استعلام البحث.
        :return: قائمة تحتوي على كائنات Document.
        """
        relevant_chunks = self.db_manager.similarity_search(query, k=self.k)
        if not relevant_chunks:
            self._last_retrieved_docs = []
            return []
        
        self._last_retrieved_docs = relevant_chunks
        return relevant_chunks
    
    def get_last_retrieved_docs(self) -> List[Document]:
        """إرجاع الوثائق التي تم استرجاعها من آخر بحث."""
        return self._last_retrieved_docs
