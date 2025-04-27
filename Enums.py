from enum import Enum, unique

@unique
class QueryType(Enum):
    VECTOR_DB = "vector_db"
    DUMMY_QUERY = "dummy_query"


@unique
class ProviderName(Enum):
    GROQ = "groq"
    TOGETHER = "together"
    OPENROUTER = "openrouter"


@unique
class RetrievalMethod(Enum):
    MAX_MARGINAL_RELEVANCE = "max_marginal_relevance_search"
    SIMILARITY_SEARCH = "similarity_search"
    HYBRID = "hybrid"
    CONTEXTUAL = "contextual"