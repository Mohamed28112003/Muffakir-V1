import streamlit as st
import os
from langchain.document_loaders import DirectoryLoader
from AnswerGenerator import *
from ChromaDBManager import *
from DocumentRetriever import *
from EmbeddingProvider import *
from LLMProvider import *
from PromptManager import *
from QueryGenerator import *
from QueryTransformer import *
from RAGGenerationPipeline import *
from RAGPipelineManager import *
from RetrieveMethods import *
from SummaryChunker import *
from TextProcessor import *
from api_keys import api_keys_qroq,api_keys_together
from Reranker import *
from CrewAgents import *  
from RAGEvaluator import *
import pandas as pd 
k = 7

print("Welcome To Evaluation.")
prompt_manager = PromptManager()
embedding_model = EmbeddingProvider() 

embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
llm_provider = LLMProvider(provider_name="together",temperature=0,api_keys=api_keys_together, model="meta-llama/Llama-3.3-70B-Instruct-Turbo")
query_transformer = QueryTransformer(llm_provider, prompt_manager)
reranker = Reranker(
        embedding_provider=embedding_model,
        reranking_method='semantic_similarity'
    )

pipeline_manager = RAGPipelineManager(
        db_path="D:\Graduation Project\Local\DB_FINAL",
        model_name=embedding_model_name,
        query_transformer=query_transformer,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        k=k,
        retrive_method="similarity_search",
        reranker=reranker
    )

print("Reading the Data ...")

# Create your DataFrame
eval_df = pd.read_csv(r"D:\Graduation Project\Local\cleaned_file.csv")
eval_df = eval_df[:5]
# Initialize the evaluator
evaluator = RAGEvaluator(
    pipeline_manager=pipeline_manager,
    llm_provider=llm_provider,
    prompt_manager=prompt_manager,
    embedding_provider=embedding_model  # Pass the embedding provider for relevance computation
)

# # Run the evaluation (you can also adjust sample_size or relevance_threshold as needed)
# results = evaluator.evaluate_chunk_retrieval_from_df(
#     eval_df=eval_df,
#     k=k,
#     sample_size=None,  # Use all rows
#     relevance_threshold=0.7  # Adjust this threshold based on your experiments
# )
## orchunk -> chunk 1 > 0.7 chunk 2 chunk 3 
# text in chunk 
# 


results = evaluator.evaluate_embedding_provider(eval_df, embedding_model, n_negative=5)

# print(f"Total Questions: {results['total_questions']}")
# print(f"Total Relevant Hits: {results['total_relevant_hits']}")
# print(f"Relevance Ratio: {results['relevance_ratio']:.2f}")
# print(f"Average Relevance Score: {results['average_relevance_score']:.2f}")