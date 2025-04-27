# Search.py

from typing import List, Dict, Any, Optional, Callable
import logging

from firecrawl import FirecrawlApp
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
from QueryTransformer.QueryTransformer import QueryTransformer
from Generation.AnswerGenerator import AnswerGenerator


class Search:

    def __init__(
        self,
        api_key: str,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        params: Dict[str, Any],
        firecrawl_app_factory: Optional[Callable[[str], FirecrawlApp]] = None,
    ):

        self.logger = logging.getLogger(__name__)
        self.params = params
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager

        if firecrawl_app_factory:
            self.firecrawl = firecrawl_app_factory(api_key)
        else:
            self.firecrawl = FirecrawlApp(api_key=api_key)

        self.query_transformer = QueryTransformer(
            llm_provider=llm_provider,
            prompt_manager=prompt_manager,
            prompt="search_query"
        )

        self.generator = AnswerGenerator(
            llm_provider=llm_provider,
            prompt_manager=prompt_manager
        )

    def deep_search(self, original_query: str) -> Dict[str, Any]:

        optimized = self.query_transformer.transform_query(original_query)
        self.logger.info(f"DeepSearch – optimized query: {optimized!r}")
        try:
            results = self.firecrawl.deep_research(
                query=optimized,
                params=self.params
            )
            return results
        except Exception as e:
            self.logger.error(f"DeepSearch failed: {e}", exc_info=True)
            raise

    def get_sources(self, deep_search_result: Dict[str, Any]) -> List[Dict[str, str]]:

        raw = deep_search_result.get("data", {}).get("sources", [])
        sources: List[Dict[str, str]] = []
        for s in raw:
            title = s.get("title", "").strip()
            url = s.get("url", "").strip()
            if title and url:
                sources.append({"title": title, "url": url})
        self.logger.debug(f"Parsed {len(sources)} sources.")
        return sources

    def search(self, original_query: str) -> Dict[str, Any]:
        """
        1) deep_search → 2) extract finalAnalysis → 3) generate answer → 4) return answer + sources
        """
        raw = self.deep_search(original_query)

        analysis = raw.get("data", {}).get("finalAnalysis", "")
        sources = self.get_sources(raw)

        try:
            answer = self.generator.generate_answer(original_query, analysis)
        except Exception as e:
            self.logger.error(f"Answer generation failed: {e}", exc_info=True)
            answer = "❌ فشل في توليد الإجابة."

        return {
            "answer": answer,
            "sources": sources
        }
