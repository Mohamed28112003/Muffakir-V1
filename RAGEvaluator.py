

from typing import Tuple, List, Dict, Optional, Any
from QueryTransformer import *
from LLMProvider import *
from langchain.schema import Document

from PromptManager import *

from ChromaDBManager import *
from RetrieveMethods import  *
from RAGPipelineManager import *

from QueryGenerator import *


class RAGEvaluator:
    def __init__(self,
                 pipeline_manager: RAGPipelineManager,
                 llm_provider: LLMProvider,
                 prompt_manager: PromptManager):
        """
        Initialize the RAG evaluator.

        Args:
            pipeline_manager (RAGPipelineManager): Instance of RAGPipelineManager
            llm_provider (LLMProvider): Instance of LLMProvider
        """
        self.pipeline_manager = pipeline_manager
        self.query_generator = QueryGenerator(llm_provider, prompt_manager)

    def evaluate_chunk_retrieval(self,
                               documents: List[Document],
                               k: int = 10,
                               sample_size: Optional[int] = None) -> Dict[str, Any]:

        if sample_size and sample_size < len(documents):
            import random
            eval_documents = random.sample(documents, sample_size)
        else:
            eval_documents = documents

        total_hits = 0
        results = []

        print(f"Starting evaluation on {len(eval_documents)} documents...")

        for i, doc in enumerate(eval_documents):
            try:
                query = self.query_generator.generate_query(doc.page_content)
                print(f"Generated query: {query}")
                print(f"Chunk :  {doc.page_content}" )

                retrieved_docs = self.pipeline_manager.query_similar_documents(query, k)

                hit = False
                retrieved_contents = retrieved_docs['documents'][0]

                original_content = doc.page_content.strip()
                for retrieved_doc in retrieved_contents:
                    retrieved_doc = retrieved_doc.strip()
                    if original_content in retrieved_doc or retrieved_doc in original_content:
                        hit = True
                        total_hits += 1
                        break

                # Store detailed results
                result = {
                    "chunk_id": i,
                    "original_content": doc.page_content,
                    "generated_query": query,
                    "retrieved_count": len(retrieved_contents),
                    "hit": hit,
                    "position": retrieved_contents.index(retrieved_doc) if hit else -1
                }
                results.append(result)

                print(f"Processed document {i+1}/{len(eval_documents)}: {'Hit' if hit else 'Miss'}")

            except Exception as e:
                print(f"Error processing document {i}: {e}")
                continue

        recall_at_k = total_hits / len(eval_documents)
        mean_reciprocal_rank = self._calculate_mrr(results)

        evaluation_results = {
            "total_documents": len(eval_documents),
            "total_hits": total_hits,
            "recall_at_k": recall_at_k,
            "mean_reciprocal_rank": mean_reciprocal_rank,
            "detailed_results": results
        }

        return evaluation_results

    def _calculate_mrr(self, results: List[Dict]) -> float:

        reciprocal_ranks = []
        for result in results:
            position = result["position"]
            if position >= 0:
                reciprocal_ranks.append(1.0 / (position + 1))
            else:
                reciprocal_ranks.append(0.0)

        return sum(reciprocal_ranks) / len(reciprocal_ranks)