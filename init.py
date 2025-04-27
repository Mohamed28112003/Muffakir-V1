
import os
from Generation.DocumentRetriever import DocumentRetriever
from RAGPipeline.RAGPipelineManager import RAGPipelineManager
from QueryClassification.QueryDocumentProcessor import QueryDocumentProcessor
from WebSearch.Search import Search
from QuizGeneration.QuizGeneration import QuizGeneration
from Embedding.EmbeddingProvider import EmbeddingProvider
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
from QueryTransformer.QueryTransformer import QueryTransformer
from HallucinationsCheck.HallucinationsCheck import HallucinationsCheck
from dotenv import load_dotenv
load_dotenv()
DEFAULT_DB_PATH = os.getenv("DB_PATH")
UPLOAD_DB_PATH = os.getenv("NEW_DB_PATH") 
OUTPUT_DIR = os.getenv("OUTPUT_DIR")  

_PROVIDER_NAME = "together"
_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
_TEMPERATURE = 0
_API_KEYS = os.getenv("TOGETHER_API_KEY")

_llm_provider = LLMProvider(
    provider_name=_PROVIDER_NAME,
    temperature=_TEMPERATURE,
    api_keys=_API_KEYS,
    model=_MODEL_NAME
)
_prompt_manager = PromptManager()


def initialize_rag_manager(db_path: str = DEFAULT_DB_PATH, collection_name: str = "Book") -> RAGPipelineManager:

    embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")

    query_transformer = QueryTransformer(_llm_provider, _prompt_manager, prompt="query_rewrite")
    query_processor = QueryDocumentProcessor(_llm_provider, _prompt_manager)
    hallucination = HallucinationsCheck(_llm_provider, _prompt_manager)

    return RAGPipelineManager(
        db_path=db_path,
        model_name=embedding_model_name,
        query_transformer=query_transformer,
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        k=5,
        retrive_method="similarity_search",
        query_processor=query_processor,
        hallucination=hallucination,
        collection_name=collection_name
    )


def initialize_search() -> Search:
    """
    Initialize and return a deep Search instance with shared LLM and PromptManager.
    """
    params = {
        "maxDepth": 3,
        "timeLimit": 180,
        "maxUrls": 10
    }
    # API key for Search - replace with secure retrieval if needed
    api_key = os.getenv("FIRE_CRAWL_API")

    return Search(
        api_key=api_key,
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        params=params
    )


def initialize_quiz(db_path: str = DEFAULT_DB_PATH, collection_name: str = "Book") -> QuizGeneration:
    """
    Initialize and return a QuizGeneration instance using shared LLM and PromptManager.
    """
    rag_manager = initialize_rag_manager(db_path, collection_name)
    doc_retriever = DocumentRetriever(rag_manager)
    return QuizGeneration(
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        retriever=doc_retriever
    )


# Example usage:
# rag_manager = initialize_rag_manager()
# searcher = initialize_search()
# quiz_gen = initialize_quiz()
