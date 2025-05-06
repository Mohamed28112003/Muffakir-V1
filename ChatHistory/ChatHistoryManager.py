from langchain.memory import ConversationBufferMemory
from typing import  Tuple
from QueryClassification.QueryDocumentProcessor import QueryDocumentProcessor
from LLMProvider.LLMProvider import LLMProvider
from PromptManager.PromptManager import PromptManager
class ChatHistoryManager:
    def __init__(self,llm_provider:LLMProvider, prompt_manager:PromptManager):
        self.llm_provider = llm_provider
        self.prompt_manager = prompt_manager
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    def store_conversation(self, user_message: str, bot_response: str):
        """Store a conversation pair in the memory."""
        self.memory.save_context({"input": user_message}, {"output": bot_response})
    
    def get_chat_history(self) -> str:
        """Get the full chat history formatted as a string."""
        messages = self.memory.load_memory_variables({}).get("chat_history", [])
        history_text = ""
        for msg in messages:
            if hasattr(msg, "content"):
                if "HumanMessage" in type(msg).__name__:
                    history_text += "المستخدم: " + msg.content + "\n"
                elif "AIMessage" in type(msg).__name__:
                    history_text += "المساعد: " + msg.content + "\n"
                else:
                    history_text += msg.content + "\n"
            else:
                history_text += str(msg) + "\n"
        return history_text
    
    def get_last_user_query(self) -> str:
        """Get only the last user query from the chat history."""
        messages = self.memory.load_memory_variables({}).get("chat_history", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and "HumanMessage" in type(msg).__name__:
                return msg.content
        return ""
    
    def get_last_bot_response(self) -> str:
        """Get only the last bot response from the chat history."""
        messages = self.memory.load_memory_variables({}).get("chat_history", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and "AIMessage" in type(msg).__name__:
                return msg.content
        return ""
    
    def get_last_exchange(self) -> Tuple[str, str]:
        """Get the last user query and bot response as a tuple."""
        last_user_query = ""
        last_bot_response = ""
        
        messages = self.memory.load_memory_variables({}).get("chat_history", [])
        ai_found = False
        
        for msg in reversed(messages):
            if hasattr(msg, "content"):
                if not ai_found and "AIMessage" in type(msg).__name__:
                    last_bot_response = msg.content
                    ai_found = True
                elif ai_found and "HumanMessage" in type(msg).__name__:
                    last_user_query = msg.content
                    break
        
        return last_user_query, last_bot_response
    
    def is_follow_up_request(self, query: str) -> bool:
        """
        Check if the current query is a follow-up request about the previous answer.
        For example: "shorten the answer", "summarize this", "make it shorter", etc.
        """
        follow_up_phrases = [
            "shorten", "shorter", "summarize", "brief", "simplify", 
            "condense", "make it short", "simplify the answer",
            "اختصر", "لخص", "باختصار", "بإيجاز"  # Arabic phrases
        ]

        
        query_lower = query.lower()
        return any(phrase in query_lower for phrase in follow_up_phrases)
    
    def clear_history(self):
        """Clear the chat history."""
        self.memory.clear()