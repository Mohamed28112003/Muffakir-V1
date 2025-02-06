from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
from langchain.schema import Document
from sklearn.metrics.pairwise import cosine_similarity
from QueryTransformer import *
from LLMProvider import *
from PromptManager import *
from ChromaDBManager import *
from RetrieveMethods import *
from RAGPipelineManager import *
import random
from EmbeddingProvider import EmbeddingProvider


def compute_cosine_similarity(text1: str, text2: str, embedding_provider: EmbeddingProvider) -> float:
    """
    Computes the cosine similarity between two texts using the provided embedding provider.
    """
    emb1 = np.array(embedding_provider.embed_single(text1))
    emb2 = np.array(embedding_provider.embed_single(text2))
    sim = cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))[0][0]
    return sim


def compute_cosine_similarity_from_embeddings(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """
    Computes the cosine similarity between two precomputed embeddings.
    """
    sim = cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))[0][0]
    return sim


class RAGEvaluator:
    def __init__(self,
                 pipeline_manager: RAGPipelineManager,
                 llm_provider: LLMProvider,
                 prompt_manager: PromptManager,
                 embedding_provider: Optional[EmbeddingProvider] = None):
        self.pipeline_manager = pipeline_manager
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.embedding_provider = embedding_provider

    def evaluate_chunk_retrieval_from_df(self,
                                         eval_df: pd.DataFrame,
                                         k: int = 10,
                                         sample_size: Optional[int] = None,
                                         relevance_threshold: float = 0.7
                                         ) -> Dict[str, Any]:
        """
        Evaluates the chunk retrieval by comparing the retrieved chunks against the original context.
        """
        if sample_size and sample_size < len(eval_df):
            eval_df = eval_df.sample(n=sample_size, random_state=42)

        total_questions = len(eval_df)
        total_relevant_hits = 0  
        relevance_scores = []    
        results = []

        print(f"Starting evaluation on {total_questions} questions...")

        for i, row in eval_df.iterrows():
            try:
                question = row['question']
                original_context = row['context'].strip()
                print(f"\nProcessing question {i+1}/{total_questions}")

                retrieved_docs: List[Document] = self.pipeline_manager.query_similar_documents(question, k)
                
                best_relevance_score = 0.0
                best_chunk = None
                best_position = -1

                for pos, doc in enumerate(retrieved_docs):
                    retrieved_text = doc.page_content.strip()

                    if self.embedding_provider is not None:
                        score = compute_cosine_similarity(original_context, retrieved_text, self.embedding_provider)
                    else:
                        score = 0.0

                    if score > best_relevance_score:
                        best_relevance_score = score
                        best_chunk = retrieved_text
                        best_position = pos

                relevance_hit = best_relevance_score >= relevance_threshold
                if relevance_hit:
                    total_relevant_hits += 1

                relevance_scores.append(best_relevance_score)

                result = {
                    "question_id": i,
                    "question": question,
                    "original_context": original_context,
                    "retrieved_count": len(retrieved_docs),
                    "best_relevance_score": best_relevance_score,
                    "relevance_hit": relevance_hit,
                    "best_chunk_position": best_position,
                    "best_chunk": best_chunk,
                    "all_retrieved_chunks": [doc.page_content for doc in retrieved_docs]
                }
                results.append(result)

                print(f"Best relevance score: {best_relevance_score:.2f} at position {best_position + 1 if best_position >= 0 else 'N/A'}")
                print(f"Marked as {'Relevant' if relevance_hit else 'Not Relevant'} (Threshold: {relevance_threshold})")

            except Exception as e:
                print(f"Error processing question {i}: {e}")
                continue

        average_relevance_score = sum(relevance_scores) / total_questions if total_questions > 0 else 0.0
        relevance_ratio = total_relevant_hits / total_questions if total_questions > 0 else 0.0

        evaluation_results = {
            "total_questions": total_questions,
            "total_relevant_hits": total_relevant_hits,
            "average_relevance_score": average_relevance_score,
            "relevance_ratio": relevance_ratio,
            "detailed_results": results
        }

        return evaluation_results

    def _calculate_mrr(self, results: List[Dict]) -> float:
        """
        Calculates the Mean Reciprocal Rank (MRR) from the retrieval results.
        """
        reciprocal_ranks = []
        for result in results:
            pos = result.get("best_chunk_position", -1)
            if pos >= 0:
                reciprocal_ranks.append(1.0 / (pos + 1))
            else:
                reciprocal_ranks.append(0.0)
        return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0

    def evaluate_embedding_provider(self,
                                    eval_df: pd.DataFrame,
                                    embedding_provider: EmbeddingProvider,
                                    n_negative: int = 1,
                                    random_seed: int = 42) -> Dict[str, Any]:
        """
        Evaluates the embedding provider by comparing cosine similarities between the question and its
        corresponding (positive) context versus randomly chosen (negative) contexts.
        """
        random.seed(random_seed)
        positive_sims = []
        negative_sims = []

        contexts = eval_df['context'].tolist()
        context_embeddings = embedding_provider.embed(contexts)

        for idx, row in eval_df.iterrows():
            question = row['question']
            pos_context = row['context']

            # Compute positive similarity using the embedding provider
            pos_sim = compute_cosine_similarity(question, pos_context, embedding_provider)
            positive_sims.append(pos_sim)

            negatives = []
            while len(negatives) < n_negative:
                neg_idx = random.randint(0, len(eval_df) - 1)
                if neg_idx != idx:
                    negatives.append(neg_idx)

            for neg_idx in negatives:
                neg_context = contexts[neg_idx]
                neg_sim = compute_cosine_similarity(question, neg_context, embedding_provider)
                negative_sims.append(neg_sim)

        avg_positive = np.mean(positive_sims)
        avg_negative = np.mean(negative_sims)

        print(f"Average Positive Similarity: {avg_positive:.3f}")
        print(f"Average Negative Similarity: {avg_negative:.3f}")

        return {
            "avg_positive_similarity": avg_positive,
            "avg_negative_similarity": avg_negative,
            "positive_similarities": positive_sims,
            "negative_similarities": negative_sims
        }
