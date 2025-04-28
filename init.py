
import os
from dotenv import load_dotenv

load_dotenv()


from config import settings
from Enums import ProviderName, RetrievalMethod

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
from YoutubeSearch.YoutubeSearch import YoutubeSearch
_llm_provider = LLMProvider(
    api_key=settings.TOGETHER_API_KEY,
    provider=settings.PROVIDER_NAME,
    model=settings.LLM_MODEL_NAME,
    temperature=0.0,
    max_tokens=500,
)

_prompt_manager = PromptManager()

# shared EmbeddingProvider (if you need it elsewhere)
_embedding_provider = EmbeddingProvider(
    model_name=settings.EMBEDDING_MODEL_NAME,
    batch_size=32,
)


def initialize_rag_manager(
    db_path: str = settings.DB_PATH,
    collection_name: str = "Book",
) -> RAGPipelineManager:
    """
    Create a RAGPipelineManager wired with all shared components.
    """
    # Query-side utilities
    query_transformer = QueryTransformer(
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        prompt="query_rewrite",
    )
    query_processor = QueryDocumentProcessor(
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
    )
    hallucination = HallucinationsCheck(
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
    )

    return RAGPipelineManager(
        db_path=db_path,
        collection_name=collection_name,
        model_name=settings.EMBEDDING_MODEL_NAME,
        llm_provider=_llm_provider,
        query_transformer=query_transformer,
        prompt_manager=_prompt_manager,
        query_processor=query_processor,
        hallucination=hallucination,
        k=settings.K,
        fetch_k=settings.FETCH_K,
        retrieve_method=settings.RETRIEVE_METHOD,
    )


def initialize_search() -> Search:
    """
    Initialize and return a Search instance with shared LLM and PromptManager.
    """

    return Search(
        api_key=settings.FIRE_CRAWL_API,
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        max_depth=3,
        time_limit=60,
        max_urls=10,
    )


def initialize_quiz(
    db_path: str = settings.DB_PATH,
    collection_name: str = "Book",
) -> QuizGeneration:

    rag_manager = initialize_rag_manager(db_path, collection_name)
    doc_retriever = DocumentRetriever(rag_manager)
    return QuizGeneration(
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
        retriever=doc_retriever,
    )




def initialize_youtube_search() -> YoutubeSearch:


    return YoutubeSearch(
        api_key=settings.FIRE_CRAWL_API,
        llm_provider=_llm_provider,
        prompt_manager=_prompt_manager,
    )