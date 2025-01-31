from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from typing import Tuple, List, Dict, Optional, Any
from langchain.schema import Document
import re

class TextProcessor:

    @staticmethod
    def split_text_recursive(documents: List[Document], chunk_size: int, chunk_overlap: int):
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(documents)

    @staticmethod
    def clean_arabic_text(text):
        text = re.sub(r'Page number: \d+', '', text)
        text = re.sub(r'- \d+ -', '', text)
        text = re.sub(r'[^؀-ۿ0-9\s]', '', text)
        text = re.sub(r'[^\w\s؀-ۿ0-9]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def clean_metadata(metadata):
        if 'source' in metadata:
            source_path = metadata['source']
            filename = source_path.split('/')[-1]
            filename_without_extension = re.sub(r'\.txt$', '', filename)
            cleaned_metadata = re.sub(r'_', ' ', filename_without_extension)
            return cleaned_metadata
        return None

    @staticmethod
    def process_documents(documents: List[Document], chunk_size: int, chunk_overlap: int):
        for doc in documents:
            doc.page_content = TextProcessor.clean_arabic_text(doc.page_content)
            if isinstance(doc.metadata, dict):
                doc.metadata['source'] = TextProcessor.clean_metadata(doc.metadata)

        doc_splits = TextProcessor.split_text_recursive(documents, chunk_size, chunk_overlap)

        for i, doc in enumerate(doc_splits):
            doc.metadata['chunk_id'] = i + 1

        return doc_splits
