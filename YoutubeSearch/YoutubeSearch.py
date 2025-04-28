from typing import List, Dict, Any
import logging
import re

from firecrawl import FirecrawlApp
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
from QueryTransformer.QueryTransformer import QueryTransformer

class YoutubeSearch:
    def __init__(
        self,
        api_key: str,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
    ):
        self.logger = logging.getLogger(__name__)
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.firecrawl = FirecrawlApp(api_key=api_key)
        self.query_transformer = QueryTransformer(
            llm_provider=llm_provider,
            prompt_manager=prompt_manager,
            prompt="youtube"
        )

    def youtube_search(self, original_query: str) -> List[Dict[str, str]]:
        optimized = self.query_transformer.transform_query(original_query)
        self.logger.info(f"YoutubeSearch – optimized query: {optimized!r}")

        try:
            results = self.firecrawl.search(
                query=optimized,
                limit=5,
            )

            formatted_results = []
            for result in results.data:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "thumbnail": self.get_youtube_thumbnail(result.get("url", ""))
                })

            return formatted_results

        except Exception as e:
            self.logger.error(f"YoutubeSearch failed: {e}", exc_info=True)
            raise

    def get_youtube_thumbnail(self, url: str) -> str:
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
        match = re.search(pattern, url)
        if not match:
            self.logger.warning(f"Invalid YouTube URL: {url}")
            return ""
        video_id = match.group(1)
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
