from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *
from PromptManager import *
from Reranker import *  
from RAGPipelineManager import RAGPipelineManager
from DocumentRetriever import *
from AnswerGenerator import *
from QueryDocumentProcessor import *
from CrewAgents import CrewAgents
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
        crewagent: CrewAgents, 
        reranker: Optional[Reranker] = None,
        k: int = 7
    ):
        self.pipeline_manager = pipeline_manager
        self.llm_provider = llm_provider
        self.query_processor = query_processor  
        self.crewagent = crewagent
        self.retriever = DocumentRetriever(pipeline_manager)
        self.generator = AnswerGenerator(llm_provider, prompt_manager)
        self.reranker = reranker or Reranker()  # Default reranker if not provided
        self.hallucination = hallucination
        self.k = k

    def generate_response(self, query: str,type:str) -> Dict[str, Any]:
        """
        Generate a response for a given query using the classification system.

        Returns:
            Dict containing the generated answer and retrieval metadata.
        """

        # Step 1: Classify the query
        query_type = self.query_processor.classify_query(query)
        db_path= self.pipeline_manager.db_path

        if query_type == "dummy_query":
            llm = self.llm_provider.get_llm()
            print("DUMMYYYY !!!!!!!!")
            answer = llm.invoke(query)

            # Directly answer with LLM
            return {
                "answer": answer.content,
                "retrieved_documents": [],
                "source_metadata": [],
            }

        elif query_type == "vector_db":
            # Retrieve documents from ChromaDB
            if (type=="agentic"):
               # db_path = "D:\Graduation Project\Local\DB_FINAL"

                agent = AgenticRag(db_path=db_path)
                response = agent.run_query(query)
                

                return {
                    "answer": response['response'],
                    "retrieved_documents": [doc.page_content for doc in response['retrieved_docs']],
                    "source_metadata": [doc.metadata for doc in response['retrieved_docs']],
                }




            retrieval_result = self.retriever.retrieve_documents(query, self.k)
            formatted_documents = self.retriever.format_documents(retrieval_result)




            # Grade the retrieved documents
           # graded_documents = self.query_processor.grade_documents(formatted_documents, query)

           
                # Rerank documents
            reranked_documents = self.reranker.rerank(query, formatted_documents)

                # Generate answer using reranked documents
            answer = self.generator.generate_answer(query, reranked_documents)

            if answer in "لا يمكنني الإجابة على هذا السؤال":
                return  {
                "answer": llm.invoke(query),
                "retrieved_documents": [],
                "source_metadata": [],
            }

            return {
                    "answer": answer,
                    "retrieved_documents": [doc.page_content for doc in reranked_documents],
                    "source_metadata": [doc.metadata for doc in reranked_documents],
                }
        elif query_type == "web_search":
                self.crewagent.user_query = query  

                self.crewagent.setup()
                self.crewagent.run()

                answer_path = os.path.join("./research", "answer.txt")
                with open(answer_path, 'r', encoding='utf-8') as f:
                    answer = f.read()
                

                answer = self.hallucination.check_answer(answer) 



                # If retrieval fails, use web search
                return {
                    "answer": answer,
                    "retrieved_documents": [],
                    "source_metadata": [],
                }



        else:
            raise ValueError(f"Unknown query type: {query_type}")