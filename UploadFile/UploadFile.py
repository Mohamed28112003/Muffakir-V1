from TextProcessor.ArabicBookProcessor import *
from RAGPipeline.RAGPipelineManager import *
from VectorDB.ChromaDBManager import *
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
load_dotenv()


new_db_path = os.getenv("NEW_DB_PATH")
output_dir = os.getenv("OUTPUT_DIR")  

class UploadFile:
    def __init__(self, path: str, model_name: str = 'mohamed2811/Muffakir_Embedding'):
        self.path = path  
        
        final_path = self.analyze_document(self.path) 

        self.processor = ArabicBookProcessor(final_path)

        self.db_manager = ChromaDBManager(
            path=new_db_path,
            collection_name="new_data",
            model_name=model_name
        )

    def upload(self):
        processed_docs = self.processor.process_documents()
        self.db_manager.add_documents(processed_docs)
        print("NEW PATH", new_db_path)
        return new_db_path

    @staticmethod
    def analyze_document(file_path):
        endpoint = "https://documentsfree.cognitiveservices.azure.com/"
        api_key = os.getenv("AZURE_API_KEY")

        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_dir, base_name + "_extracted.txt")

        with open(file_path, "rb") as document:
            poller = document_analysis_client.begin_analyze_document(
                model_id="prebuilt-layout",
                document=document)
            
            result = poller.result()

            with open(output_file, "w", encoding="utf-8") as text_file:
                print(f"Total pages: {len(result.pages)}", file=text_file)
                
                for page in result.pages:
                    print(f"\nPage number: {page.page_number}\n", file=text_file)
                    for line in page.lines:
                        print(line.content, file=text_file)

        return output_dir
    



