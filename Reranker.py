import numpy as np
from typing import List, Optional, Tuple
from langchain.schema import Document
from EmbeddingProvider import EmbeddingProvider
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(
        self, 
        embedding_provider: Optional[EmbeddingProvider] = None, 
        model_name: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        reranking_method: str = 'semantic_similarity',
        cross_encoder_model_name: Optional[str] = None
    ):
        """
        Initializes the reranker.
        
        Args:
            embedding_provider (Optional[EmbeddingProvider]): Embedding provider instance. If None, a new instance will be created using the provided model_name.
            model_name (str): The name of the model for generating embeddings.
            reranking_method (str): The method to use for reranking. Options are 'semantic_similarity', 'bm25', 'hybrid', or 'cross_encoder'.
            cross_encoder_model_name (Optional[str]): The model name for the cross-encoder reranker. Only used if reranking_method=='cross_encoder'.
        """
        self.embedding_provider = embedding_provider if embedding_provider is not None else EmbeddingProvider(model_name)
        self.reranking_method = reranking_method
        
        # If using cross-encoder reranking, load the model.
        if self.reranking_method == 'cross_encoder':
            # Provide a default cross encoder model if none is given.
            cross_encoder_model_name = cross_encoder_model_name or 'cross-encoder/ms-marco-MiniLM-L-6-v2'
            self.cross_encoder = CrossEncoder(cross_encoder_model_name)
        else:
            self.cross_encoder = None

    def compute_semantic_similarity(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        """
        Compute ranking based on semantic similarity using document embeddings.
        """
        query_embedding = self.embedding_provider.embed_query(query)
        document_embeddings = [
            self.embedding_provider.embed_single(doc.page_content) 
            for doc in documents
        ]
     
        similarities = [
            np.dot(query_embedding, doc_emb) / 
            (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            for doc_emb in document_embeddings
        ]
        
        return sorted(
            zip(documents, similarities), 
            key=lambda x: x[1], 
            reverse=True
        )

    def compute_bm25_ranking(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        """
        Compute BM25 ranking for documents.
        
        Args:
            query (str): Input query.
            documents (List[Document]): List of documents.
        
        Returns:
            List of tuples with (document, BM25 score).
        """
        # Tokenize documents and query.
        tokenized_docs = [doc.page_content.split() for doc in documents]
        tokenized_query = query.split()
        
        # Create BM25 ranker.
        bm25 = BM25Okapi(tokenized_docs)
        
        # Score documents.
        doc_scores = bm25.get_scores(tokenized_query)
        
        return sorted(
            zip(documents, doc_scores), 
            key=lambda x: x[1], 
            reverse=True
        )

    def compute_hybrid_ranking(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        """
        Compute a hybrid ranking that combines semantic similarity and BM25 scores.
        """
        semantic_scores = self.compute_semantic_similarity(query, documents)
        bm25_scores = self.compute_bm25_ranking(query, documents)
        
        # Normalize and combine scores.
        hybrid_scores = []
        for (doc, sem_score), (_, bm25_score) in zip(semantic_scores, bm25_scores):
            hybrid_score = 0.6 * sem_score + 0.4 * bm25_score
            hybrid_scores.append((doc, hybrid_score))
        
        return sorted(hybrid_scores, key=lambda x: x[1], reverse=True)

    def compute_cross_encoder_ranking(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        """
        Compute ranking using a cross-encoder model.
        
        Args:
            query (str): Input query.
            documents (List[Document]): List of documents.
            
        Returns:
            List of tuples with (document, cross-encoder score).
        """
        if self.cross_encoder is None:
            raise ValueError("Cross encoder model not initialized.")
        
        # Create pairs of (query, document_text) for each document.
        query_candidate_pairs = [(query, doc.page_content) for doc in documents]
        
        # Get relevance scores from the cross-encoder.
        scores = self.cross_encoder.predict(query_candidate_pairs)
        
        return sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)

    def rerank(
        self, 
        query: str, 
        documents: List[Document], 
        top_k: Optional[int] = None
    ) -> List[Document]:
        """
        Reranks the provided documents based on the chosen method.
        
        Args:
            query (str): Input query.
            documents (List[Document]): List of candidate documents.
            top_k (Optional[int]): The number of top documents to return.
        
        Returns:
            List of top_k reranked Document objects.
        """
        if not documents:
            return []
        
        top_k = top_k or len(documents)
        
        # Select the reranking method.
        if self.reranking_method == 'semantic_similarity':
            ranked_docs = self.compute_semantic_similarity(query, documents)
        elif self.reranking_method == 'bm25':
            ranked_docs = self.compute_bm25_ranking(query, documents)
        elif self.reranking_method == 'hybrid':
            ranked_docs = self.compute_hybrid_ranking(query, documents)
        elif self.reranking_method == 'cross_encoder':
            ranked_docs = self.compute_cross_encoder_ranking(query, documents)
        else:
            raise ValueError(f"Unknown reranking method: {self.reranking_method}")
        
        # Return top_k documents.
        return [doc for doc, _ in ranked_docs]
