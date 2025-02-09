from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from tavily import TavilyClient
from HallucinationsCheck import *



SAMBANOVA_API_KEY = "abaaebe1-f9a2-4374-96da-a91630c7e113"
TAVILY_API_KEY = "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"

llm = LLM(
    model="sambanova/Meta-Llama-3.3-70B-Instruct",
    temperature=0,
    api_key=SAMBANOVA_API_KEY
)

@tool
def search_engine_tool(query: str) -> str:
    """
    Perform a web search using the Tavily API and return the search context.

    Args:
        query (str): The search query string.

    Returns:
        str: The search context retrieved from the Tavily API.
    """
    client = TavilyClient(api_key=TAVILY_API_KEY)
    return client.get_search_context(query)

@tool
def read_context_file(file_path: str) -> str:
    """
    Read the content of a text file and return it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


class CrewAgents:
    def __init__(self, user_query: str, country: str, language: str, output_dir: str = "./output"):
        self.user_query = user_query
        self.country = country
        self.language = language
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _create_search_agent(self) -> Agent:
        return Agent(
            role="Legal Research Analyst",
            goal=f"""Conduct comprehensive legal research for {self.country} in {self.language} 
                    regarding: {self.user_query}""",
            backstory="A specialized legal research assistant with expertise in finding and analyzing legal sources.",
            tools=[search_engine_tool],
            llm=llm,
            verbose=True
        )

    def _create_answer_agent(self) -> Agent:
        return Agent(
            role="Legal Documentation Specialist",
            goal="Generate clear, accurate legal answers with proper citations",
            backstory="Experienced legal writer skilled in creating authoritative legal documents.",
            tools=[read_context_file],
            llm=llm,
            verbose=True
        )

    def _create_search_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
                Conduct legal research about: {self.user_query}
                Focus on jurisdiction: {self.country}
                Language requirements: {self.language}
                
                Required Steps:
                1. Perform comprehensive search using legal databases
                2. Filter results by jurisdiction and relevance
                3. Organize findings into structured format
                4. Get links of the resource 
                
            """,
            expected_output="Structured text file with legal references links and key findings",
            output_file=os.path.join(self.output_dir, "research_results.txt"),
            agent=agent
        )

    def _create_answer_task(self, agent: Agent) -> Task:
        return Task(
            description=f"""
                Generate legal answer for: {self.user_query}
                Use research from: {os.path.join(self.output_dir, "research_results.txt")}
                
                Requirements:
                - Answer in {self.language} only
                - Cite relevant laws from {self.country}
                - Use academic formatting
                - Generate responses only using the provided context. Do not speculate, assume, or invent details or any language.
                
            """,
            expected_output="Well-structured legal answer and legal references links in .txt format",
            output_file=os.path.join(self.output_dir, "answer.txt"),
            agent=agent,
            context=[self.research_task]
        )

    def setup(self):
        self.research_agent = self._create_search_agent()
        self.answer_agent = self._create_answer_agent()
        
        self.research_task = self._create_search_task(self.research_agent)
        self.answer_task = self._create_answer_task(self.answer_agent)
        
        self.crew = Crew(
            agents=[self.research_agent, self.answer_agent],
            tasks=[self.research_task, self.answer_task],
            process=Process.sequential,

            verbose=True
        )

    def run(self) -> str:
        return self.crew.kickoff()
    
  