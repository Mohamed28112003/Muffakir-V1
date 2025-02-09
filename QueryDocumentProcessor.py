from PromptManager import *
from LLMProvider import *
class QueryDocumentProcessor:
    def __init__(self, llm_provider:LLMProvider, prompt_manager: PromptManager):

        self.llm_provider = llm_provider
        self.query_classification_prompt = prompt_manager.get_prompt("query_classification_prompt")

    def classify_query(self, query: str) -> str:
        try:
            llm = self.llm_provider.get_llm()
            prompt = self.query_classification_prompt.format(query_transformed=query) ## propt
            response = llm.invoke(prompt)

            if hasattr(response, 'content'):
                print("classsss !!!! ", response.content)
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            print(f"Error transforming query: {e}")
            print("Switching API key and retrying QUERY...")
            self.llm_provider.switch_api_key()
            return self.classify_query(query)

    def grade_documents(self, documents, query: str):
        graded_documents = []
        for doc in documents:
            response = self.llm.invoke(self.prompt_manager.document_grading_prompt_template.format(
                document=doc.page_content, question=query
            ))
            if response['binary_score'] == 'yes':
                graded_documents.append(doc)
        return graded_documents