from langchain.schema import Document
from typing import Tuple, List, Dict, Optional, Any
from sentence_transformers import util

import numpy as np

class ChunkEvaluator:
    def __init__(self, similarity_model, query_generator, summary_chunker):

        self.similarity_model = similarity_model
        self.query_generator = query_generator
        self.summary_chunker = summary_chunker

    def compute_similarity(self, query: str, chunks: List[str]) -> List[float]:

        query_embedding = self.similarity_model.encode(query, convert_to_tensor=True)
        chunk_embeddings = self.similarity_model.encode(chunks, convert_to_tensor=True)
        return util.cos_sim(query_embedding, chunk_embeddings)[0].tolist()

    def evaluate_chunk(self, chunk: str, document_title: str) -> Tuple[float, float]:

        query = self.query_generator.generate_query(chunk)
        chunk_wo_header = chunk
        chunk_w_header = f"ملخص: {document_title}\n\n{chunk}"

        # Print both the chunk with and without the header
        print("\nChunk without header:")
        print(chunk_wo_header)
        print("\nChunk with header:")
        print(chunk_w_header)

        similarity_scores = self.compute_similarity(query, [chunk_wo_header, chunk_w_header])
        return similarity_scores[0], similarity_scores[1]

    def evaluate_all_chunks(self, documents: List[str], titles: List[str]) -> Tuple[float, float]:

        scores_without_header = []
        scores_with_header = []

        for i, (chunk, title) in enumerate(zip(documents, titles)):
            try:
                similarity_wo_header, similarity_w_header = self.evaluate_chunk(chunk, title)
                scores_without_header.append(similarity_wo_header)
                scores_with_header.append(similarity_w_header)

                print(f"\nChunk {i + 1}:")
                print(f"Generated Query: {self.query_generator.generate_query(chunk)}")
                print(f"Similarity without header: {similarity_wo_header:.4f}")
                print(f"Similarity with header: {similarity_w_header:.4f}")

            except Exception as e:
                print(f"Error processing chunk {i + 1}: {e}")
                continue

        avg_without = np.mean(scores_without_header) if scores_without_header else 0
        avg_with = np.mean(scores_with_header) if scores_with_header else 0

        print(f"\nFinal Results:")
        print(f"Average similarity without headers: {avg_without:.4f}")
        print(f"Average similarity with headers: {avg_with:.4f}")
        if avg_without:
            print(f"Improvement with headers: {((avg_with - avg_without) / avg_without * 100):.2f}%")

        return avg_without, avg_with
