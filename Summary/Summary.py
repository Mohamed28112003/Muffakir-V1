from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_transformers import EmbeddingsClusteringFilter
from langchain.prompts import PromptTemplate
from typing import List, Dict, Optional, Any
import os
from Enums import SummaryStrategy

from Embedding.EmbeddingProvider import EmbeddingProvider
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager





class Summarizer:
    """Class to handle document summarization using different strategies"""
    
    def __init__(
        self,
        llm_provider: LLMProvider,
        embedding_provider: EmbeddingProvider,
        prompt_manager: Optional[PromptManager] = None,
        max_chunk_limit: int = 300,
    ):
        """
        Initialize the summarizer with necessary components
        
        Args:
            llm_provider: LLM provider for text generation
            embedding_provider: Embedding provider for text embeddings
            prompt_manager: Optional prompt manager for templating
            max_chunk_limit: Maximum number of chunks allowed for processing
        """
        self.llm_provider = llm_provider
        self.embedding_provider = embedding_provider
        self.prompt_manager = prompt_manager
        self.max_chunk_limit = max_chunk_limit
        

    
    def extract(self, file_path: str, chunk_size: int = 800, chunk_overlap: int = 150):
        """
        Extract and split text from PDF file
        
        Args:
            file_path: Path to the PDF file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of document chunks
        """
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        texts = text_splitter.split_documents(pages)
        return texts
    
    def adaptive_clustering(self, texts, min_clusters: int = 2, max_clusters: int = 5):
        """
        Adaptively choose the number of clusters based on document size
        
        Args:
            texts: List of text chunks
            min_clusters: Minimum number of clusters
            max_clusters: Maximum number of clusters
            
        Returns:
            Number of clusters to use
        """
        num_chunks = len(texts)
        
        if num_chunks < min_clusters:
            num_clusters = min_clusters
        elif num_chunks >= max_clusters:
            num_clusters = max_clusters
        else:
            num_clusters = num_chunks - 1
            
        return num_clusters
    
    def summarize(self, file_path: str, strategy: SummaryStrategy = SummaryStrategy.AUTO) -> Dict[str, Any]:
        """
        Summarize a document using the specified strategy
        
        Args:
            file_path: Path to the PDF file
            strategy: Strategy to use for summarization
            
        Returns:
            Dictionary with summary and metadata
        """
        try:
            # Extract text chunks from PDF
            texts = self.extract(file_path)
            num_chunks = len(texts)
            
            # Check if document exceeds chunk limit
            if num_chunks > self.max_chunk_limit:
                return {
                    "success": False,
                    "error": f"File too large: contains {num_chunks} chunks, maximum allowed is {self.max_chunk_limit}",
                    "summary": None
                }
            
            # Determine strategy if AUTO
            if strategy == SummaryStrategy.AUTO:
                if num_chunks < 6:
                    strategy = SummaryStrategy.DIRECT
                else:
                    strategy = SummaryStrategy.CLUSTERING
            
            # Apply the selected strategy
            if strategy == SummaryStrategy.DIRECT:
                summary = self._direct_summarize(texts)
            else:  # CLUSTERING
                summary = self._clustering_summarize(texts)
            
            return {
                "success": True,
                "chunks": num_chunks,
                "strategy": strategy.value,
                "summary": summary
            }
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return {
                "success": False,
                "error": str(e),
                "details": error_details,
                "summary": None
            }
    
    def _get_prompt(self, prompt_key: str) -> PromptTemplate:
        """Get prompt from manager or use default"""
        if self.prompt_manager:
            try:
                template = self.prompt_manager.get_prompt(prompt_key)
                return PromptTemplate(template=template, input_variables=["text"])
            except (ValueError, KeyError):
                # Fallback to default template if prompt not found
                pass
        
        return print(f"Prompt '{prompt_key}' not found in PromptManager. Using default template.")
    
    def _direct_summarize(self, texts):
        """Summarize directly using refine chain for small documents"""
        prompt = self._get_prompt("summary_direct")
        
        chain = load_summarize_chain(
            self.llm_provider.get_llm(),
            chain_type="refine",
            question_prompt=prompt,
            refine_prompt=prompt,
        )
        
        summary = chain.invoke({"input_documents": texts})
        return summary["output_text"]
    
    def _clustering_summarize(self, texts):
        """Summarize using K-means clustering approach for larger documents"""
        # Get prompts
        map_prompt = self._get_prompt("summary_map")
        combine_prompt = self._get_prompt("summary_combine")
        
        # Determine optimal number of clusters
        num_clusters = self.adaptive_clustering(texts)
        
        # Apply clustering filter
        filter = EmbeddingsClusteringFilter(
            embeddings=self.embedding_provider,
            num_clusters=num_clusters
        )
        
        filtered_texts = filter.transform_documents(documents=texts)
        
        # Small check - if filtering fails or produces too few results, fall back to direct summarization
        if len(filtered_texts) < 2:
            return self._direct_summarize(texts)
        
        # Create a map_reduce chain with appropriate prompts
        chain = load_summarize_chain(
            self.llm_provider.get_llm(),
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt,
        )
        
        summary = chain.invoke({"input_documents": filtered_texts})
        return summary["output_text"]

    def save_summary(self, summary_text: str, output_path: str = "summary.txt"):
        """Save summary to a file"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        return output_path