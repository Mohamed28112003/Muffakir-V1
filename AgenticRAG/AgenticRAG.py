from crewai import Agent, Task, Crew, Process, LLM
from AgenticRAG.DocumentSearchTool import DocumentSearchTool  
from typing import Tuple, Dict, Any

class AgenticRag:

    def __init__(self, db_path: str, k: int = 5):

        self.db_path = db_path
        self.k = k
        self.crew = self.create_agents_and_tasks()
        self.retrieved_docs = None

    def load_llm(self) -> LLM:

        SAMBANOVA_API_KEY = "abaaebe1-f9a2-4374-96da-a91630c7e113"
        return LLM(
            model="sambanova/Meta-Llama-3.3-70B-Instruct",
            temperature=0,
            api_key=SAMBANOVA_API_KEY
        )

    def create_agents_and_tasks(self) -> Crew:

        pdf_search_tool = DocumentSearchTool(db_path=self.db_path, k=self.k)
        self.search_tool = pdf_search_tool 

        retriever_agent = Agent(
            role="Information Retriever",
            goal=(
                "Retrieve relevant information from the document for the query: {query}. "
                "Use the PDF search tool to find the most pertinent information."
            ),
            backstory=(
                "You're a meticulous analyst with a keen eye for detail. "
                "You're known for your ability to understand queries and retrieve "
                "precise, relevant information from documents."
            ),
            verbose=True,
            tools=[pdf_search_tool],
            llm=self.load_llm()
        )

        # Create the response synthesizer agent
        response_synthesizer_agent = Agent(
            role="Response Synthesizer",
            goal=(
                "Create a clear, coherent response using the retrieved information. "
                "If no relevant information is available, acknowledge this politely."
                "Make it in arabic only"
            ),
            backstory=(
                "You're a skilled communicator who excels at synthesizing complex "
                "information into clear, concise, and helpful responses."
            ),
            verbose=True,
            llm=self.load_llm()
        )

        # Define the retrieval task
        retrieval_task = Task(
            description=(
                "Search the document and retrieve relevant information for: {query}\n"
                "Make sure to capture all pertinent details that could help answer the query."
            ),
            expected_output=(
                "A comprehensive collection of relevant text passages from the document "
                "that address the query, formatted as a string with clear separation "
                "between different passages."
            ),
            agent=retriever_agent
        )

        # Define the response synthesis task
        response_task = Task(
            description=(
                "Using the retrieved information, create a comprehensive response for: {query}\n"
                "If no relevant information was found, politely inform the user."
                "Make it in arabic only"
            ),
            expected_output=(
                "A clear, well-structured response that directly answers the query based in arabic only "
                "on the retrieved information. If no relevant information was found, "
                "a polite message indicating this."
            ),
            agent=response_synthesizer_agent
        )

        # Create and return the crew
        return Crew(
            agents=[retriever_agent, response_synthesizer_agent],
            tasks=[retrieval_task, response_task],
            process=Process.sequential,
            verbose=True
        )

    def run_query(self, query: str) -> Dict[str, Any]:

        try:
            result = self.crew.kickoff(inputs={"query": query})
            
            retrieved_docs = self.search_tool.get_last_retrieved_docs()
            
            return {
                "response": result.raw,
                "retrieved_docs": retrieved_docs
            }
        except Exception as e:
            error_msg = f"An error occurred while processing your query: {str(e)}"
            return {
                "response": error_msg,
                "retrieved_docs": []
            }

