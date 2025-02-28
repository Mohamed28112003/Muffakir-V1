from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import re
from typing import List, Dict
import os

from TextProcessor import *

class ArabicBookProcessor:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.text_processor = TextProcessor()

    def load_documents(self) -> List[Document]:
        """Load all text documents from the directory"""
        loader = DirectoryLoader(
            self.directory_path,
            glob="*.txt",
            show_progress=True
        )
        return loader.load()

    def split_by_pages(self, documents: List[Document]) -> List[Document]:
        """Split documents by page markers and preserve metadata"""
        page_documents = []

        for doc in documents:
            original_metadata = doc.metadata


            pages = re.split(r'(?=رقم الصفحه|Page number)', doc.page_content)

            for page in pages:
                if not page.strip():
                    continue

                page_number = None

                arabic_match = re.search(r'رقم الصفحه\s*:\s*(\d+)', page)
                if arabic_match:
                    page_number = arabic_match.group(1)
                    page = re.sub(r'رقم الصفحه\s*:\s*\d+\s*', '', page)

                english_match = re.search(r'Page number:\s*(\d+)', page)
                if english_match:
                    page_number = english_match.group(1)
                    page = re.sub(r'Page number:\s*\d+\s*', '', page)

                if page_number:
                    new_metadata = original_metadata.copy()
                    new_metadata['page_number'] = page_number

                    file_name = os.path.basename(original_metadata.get('source', ''))
                    book_name = os.path.splitext(file_name)[0]

                    new_metadata['source'] = f" اسم الكتاب : {book_name} - رقم الصفحه : {page_number}"

                    page_doc = Document(
                        page_content=page.strip(),
                        metadata=new_metadata
                    )
                    page_documents.append(page_doc)

        return page_documents

    def process_documents(self, chunk_size: int = 600, chunk_overlap: int = 200) -> List[Document]:

        documents = self.load_documents()

        page_documents = self.split_by_pages(documents)

        final_documents = self.text_processor.process_documents(
            documents=page_documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        return final_documents