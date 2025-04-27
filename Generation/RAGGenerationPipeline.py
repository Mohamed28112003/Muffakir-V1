from typing import Tuple, List, Dict, Optional, Any
from LLMProvider.LLMProvider import *
from PromptManager.PromptManager import *
from Reranker.Reranker import *  
from RAGPipeline.RAGPipelineManager import RAGPipelineManager
from Generation.DocumentRetriever import *
from Generation.AnswerGenerator import *
from QueryClassification.QueryDocumentProcessor import *
from HallucinationsCheck.HallucinationsCheck import *
from WebSearch.Search import Search
from dotenv import load_dotenv
import os
load_dotenv()
class RAGGenerationPipeline:

    def __init__(
        self,
        pipeline_manager: RAGPipelineManager,
        llm_provider: LLMProvider,
        prompt_manager: PromptManager,
        query_processor: QueryDocumentProcessor,
        hallucination : HallucinationsCheck,
        
        k: int = 5
    ):
        self.pipeline_manager = pipeline_manager
        self.llm_provider = llm_provider
        self.query_processor = query_processor
        self.retriever = DocumentRetriever(pipeline_manager)
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        
        self.query_transformer = QueryTransformer(llm_provider, prompt_manager,prompt="search_query")

        self.hallucination = hallucination
        self.k = k

    def generate_response(self, query: str,type:str) -> Dict[str, Any]:
       

  



    

        query_type = self.query_processor.classify_query(query=query)


        print("query_type = ",query_type)



        if query_type == "dummy_query":
            llm = self.llm_provider.get_llm()
            print("DUMMYYYY !!!!!!!!")
            answer = llm.invoke(query)
            answer = self.hallucination.check_answer(answer.content)



            return {
                "answer": answer,
                "retrieved_documents": [],
                "source_metadata": [],
            }

        elif query_type == "vector_db":

            retrieval_result = self.retriever.retrieve_documents(query, self.k)

            formatted_documents = self.retriever.format_documents(retrieval_result)


            answer = self.generator.generate_answer(query, formatted_documents)


            if answer in "لا يمكنني الإجابة على هذا السؤال":
                llm = self.llm_provider.get_llm()
                optimized_query = self.query_transformer.transform_query(query)

                print("optimized_query in no answer",optimized_query)
                params = {
                "maxDepth": 3,
                "timeLimit": 30,
                "maxUrls": 5
                    }
                search_instance=  Search(
                    api_key=os.getenv("FIRE_CRAWL_API"),
                    llm_provider=self.llm_provider,
                    prompt_manager=self.prompt_manager,
                    params=params
                                )
                
                results = search_instance.deep_search(optimized_query)
                final_analysis = results["data"].get("finalAnalysis", "لا يوجد تحليل متاح.")
                sources = results["data"].get("sources", [])



                
                response = llm.invoke(optimized_query)
                answer = self.hallucination.check_answer(response.content)


                print("HERE NO ANSWER !!!!!")
                self.pipeline_manager.store_conversation(query, answer)


                return  {

                "answer": final_analysis,
                "retrieved_documents": [],
                "source_metadata": sources,
            }




            return {
                    "answer": answer,
                    "retrieved_documents": [doc.page_content for doc in formatted_documents],
                    "source_metadata": [doc.metadata for doc in formatted_documents],
                }



        else:
            raise ValueError(f"Unknown query type: {query_type}")