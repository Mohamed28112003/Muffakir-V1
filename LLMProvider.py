from typing import Tuple, List, Dict, Optional, Any
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI  

class LLMProvider:
    def __init__(self, api_keys: List[str], provider_name:str, model: str, temperature: float = 0.5, max_tokens: int = 300):
        self.api_keys = api_keys
        self.api_key_index = 0
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.provider_name=provider_name

        self.llm = self.initialize_llm()

    def initialize_llm(self):
        if self.provider_name =="groq":
         
            return ChatGroq(
                api_key=self.api_keys[self.api_key_index],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        elif self.provider_name=="together" :
            
            return   ChatOpenAI(
        openai_api_key=self.api_keys[self.api_key_index],
        model=self.model,
        temperature=self.temperature,
         max_tokens=self.max_tokens,

        openai_api_base="https://api.together.xyz/v1"
    )
        else :
            raise ValueError(f"Unknown retrive_method: {self.self.provider_name}")

        



    def get_llm(self):
        return self.llm

    def switch_api_key(self):
        print(f"Switching from API key index {self.api_key_index}")
        self.api_key_index = (self.api_key_index + 1) % len(self.api_keys)
        self.llm = self.initialize_llm()
        print(f"Switched to API key index {self.api_key_index}")
        return self.llm