from PromptManager.PromptManager import *
from LLMProvider.LLMProvider import *
from Enums import QueryType

class QueryDocumentProcessor:
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.query_classification_prompt = prompt_manager.get_prompt("query_classification_prompt")

    def classify_query(self, query: str) -> str:
        try:
            llm = self.llm_provider.get_llm()
            prompt = self.query_classification_prompt.format(query_transformed=query)
            response = llm.invoke(prompt)
            if hasattr(response, 'content'):
                print("classsss !!!! ", response.content)
                return response.content.strip()
            elif isinstance(response, str):
                return response.strip()
            else:
                return str(response).strip()
        except Exception as e:
            print(f"Error QueryDocumentProcessor transforming query: {e}")


    def classify_query_with_history(self, chat_history: str, new_query: str) -> str:
        """
        Determine if a query depends on chat history or is a standalone query.
        
        Args:
            chat_history: The full chat history as a formatted string
            new_query: The new query to classify
            
        Returns:
            'history' if the query depends on previous context, 'original' otherwise
        """
        try:
            # Get the history classification prompt
            prompt = self.prompt_manager.get_prompt("history_classification_prompt")
            
            # Format the prompt with the chat history and new query
            formatted_prompt = prompt.format(
                conversation_history=chat_history,
                new_query=new_query
            )
            
            # Send the prompt to the LLM
            llm = self.llm_provider.get_llm()
            response = llm.invoke(formatted_prompt)
            
            # Extract the classification from the structured output
            classification = self._extract_classification(response)
            
            print(f"Query classification: {classification}")
            
            # Map the raw classification to QueryType enum values
            if classification == "history":
                return QueryType.HiSTORY_QUERY.value
            else:  # Default to "original" for any other response
                return QueryType.ORIGINAL_QUERY.value
                
        except Exception as e:
            print(f"Error in classify_query_with_history: {e}")
            # Default to original query in case of errors
            return QueryType.ORIGINAL_QUERY.value
    
    def _extract_classification(self, response) -> str:
        """
        Extract the classification from the structured XML response.
        
        Expected format: <output><classification>VALUE</classification></output>
        """
        try:
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to extract from XML structure
            import re
            match = re.search(r'<classification>(.*?)</classification>', response_text, re.DOTALL)
            
            if match:
                # Return the classification value, trimmed of whitespace
                return match.group(1).strip().lower()
            
            # If we can't extract from XML, check if the raw response is just "history" or "original"
            response_text = response_text.strip().lower()
            if response_text in ["history", "original"]:
                return response_text
            
            # Default to "original" if parsing fails
            return "original"
        except Exception as e:
            print(f"Error extracting classification: {e}")
            return "original"