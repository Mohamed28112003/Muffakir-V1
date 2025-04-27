from sentence_transformers import SentenceTransformer
from typing import  List


class EmbeddingProvider:
    def __init__(self, model_name: str = 'mohamed2811/Muffakir_Embedding'):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

    def embed_single(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """ This method is required by LangChain's Chroma integration """
        return self.embed(texts)

    def embed_query(self, query: str) -> List[float]:
        """ This method is required for processing queries in LangChain """
        return self.embed_single(query)
