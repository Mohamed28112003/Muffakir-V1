from typing import Tuple

class QueryClassifier:
    """
    Classifies a transformed query into one of three categories:
    - 'vector_db': Exists in the vector database.
    - 'web_search': Requires a web search.
    - 'dummy_query': Casual or irrelevant question.
    """

    def __init__(self, vector_retriever, tavily_agent, llm_provider, prompt_manager):
        self.vector_retriever = vector_retriever
        self.tavily_agent = tavily_agent
        self.llm_provider = llm_provider
        self.classification_prompt = prompt_manager.get_prompt("query_classification")

    def classify_query(self, query_transformed: str) -> Tuple[str, str]:
        """
        Classifies the query and returns the category and explanation.

        Args:
            query_transformed (str): The transformed query.

        Returns:
            Tuple[str, str]: Category and explanation.
        """
        # Check if the query exists in the vector database
        if self.vector_retriever.query_exists(query_transformed):
            return "vector_db", "Query matches content in the vector database."

        # Use LLM to classify between 'web_search' and 'dummy_query'
        llm = self.llm_provider.get_llm()
        prompt = self.classification_prompt.format(query_transformed=query_transformed)

        try:
            response = llm.invoke(prompt)
            if "web_search" in response.lower():
                return "web_search", "Query requires web search."
            return "dummy_query", "Query is a casual or irrelevant question."
        except Exception as e:
            print(f"Error classifying query: {e}")
            return "error", "An error occurred during classification."