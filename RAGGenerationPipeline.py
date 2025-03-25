from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *
from PromptManager import *
from Reranker import *  
from RAGPipelineManager import RAGPipelineManager
from DocumentRetriever import *
from AnswerGenerator import *
from QueryDocumentProcessor import *
from HallucinationsCheck import *

class RAGGenerationPipeline:
    """Main class for handling the complete RAG generation pipeline with reranking"""

    def __init__(
        self,
        pipeline_manager: RAGPipelineManager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        query_processor: QueryDocumentProcessor,
        hallucination : HallucinationsCheck,
        reranker: Optional[Reranker] = None,
        k: int = 7
    ):
        self.pipeline_manager = pipeline_manager
        self.llm_provider = llm_provider
        self.query_processor = query_processor
        self.retriever = DocumentRetriever(pipeline_manager)
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        self.reranker = reranker or Reranker()
        self.hallucination = hallucination
        self.k = k

    def generate_response(self, query: str,type:str) -> Dict[str, Any]:
        chat_history = self.pipeline_manager.get_chat_history()

        full_query = f"المحادثة السابقة:\n{chat_history}\n\nالسؤال الحالي: {query}"

  



        print(chat_history)

        print(f"input : {full_query}")


        query_type = "vector_db"

        history_type = "original"

        print("HISOTRY TYPE = ",history_type)

        if history_type == "original":

          print("original !!!!!!!!!!!!!!!!!!!")
          full_query=query

        elif history_type == "history":
          print("history !!!!!!!!!!!!!!!!!")
          full_query=full_query



        db_path= self.pipeline_manager.db_path

        if query_type == "dummy_query":
            llm = self.llm_provider.get_llm()
            print("DUMMYYYY !!!!!!!!")
            answer = llm.invoke(full_query)
            answer = self.hallucination.check_answer(answer.content)
            self.pipeline_manager.store_conversation(query, answer)



            # Directly answer with LLM
            return {
                "answer": answer,
                "retrieved_documents": [],
                "source_metadata": [],
            }

        elif query_type == "vector_db":

            retrieval_result = self.retriever.retrieve_documents(full_query, self.k)

            formatted_documents = self.retriever.format_documents(retrieval_result)

            #reranked_documents = self.reranker.rerank(query, formatted_documents)

            answer = self.generator.generate_answer(full_query, formatted_documents)
            #answer = "لا يمكنني الإجابة على هذا السؤال"

            print("DOOOOOCSSSS ::: ",formatted_documents )

            if answer in "لا يمكنني الإجابة على هذا السؤال":
                llm = self.llm_provider.get_llm()

                
                response = llm.invoke(full_query)
                answer = self.hallucination.check_answer(response.content)


                print("HERE NO ANSWER !!!!!")
                self.pipeline_manager.store_conversation(query, answer)


                return  {

                "answer": answer,
                "retrieved_documents": [],
                "source_metadata": [],
            }


            self.pipeline_manager.store_conversation(query, answer)


            return {
                    "answer": answer,
                    "retrieved_documents": [doc.page_content for doc in formatted_documents],
                    "source_metadata": [doc.metadata for doc in formatted_documents],
                }



        else:
            raise ValueError(f"Unknown query type: {query_type}")