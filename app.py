import streamlit as st
import os
from langchain.document_loaders import DirectoryLoader
from AnswerGenerator import *
from ChromaDBManager import *
from DocumentRetriever import *
from EmbeddingProvider import *
from LLMProvider import *
from PromptManager import *
from QueryGenerator import *
from QueryTransformer import *
from RAGGenerationPipeline import *
from RAGPipelineManager import *
from RetrieveMethods import *
from SummaryChunker import *
from TextProcessor import *
from api_keys import api_keys_qroq, api_keys_together
from Reranker import *
from CrewAgents import *
from HallucinationsCheck import *
from QuizGeneration import *






def initialize_rag_manager():
    """Initialize the RAG pipeline manager with memory support."""
    embedding_model_name = "mohamed2811/Muffakir_Embedding"
    
    llm_provider = LLMProvider(
        provider_name="together",
        temperature=0,
        api_keys=api_keys_together,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
    )
    
    prompt_manager = PromptManager()
    query_transformer = QueryTransformer(llm_provider, prompt_manager)
    query_processor = QueryDocumentProcessor(llm_provider, prompt_manager)
    hallucination = HallucinationsCheck(llm_provider, prompt_manager)
    crewagent = CrewAgents(
        user_query="query",
        country="Egypt",
        language="Arabic",
        output_dir="./research"
    )
    
    return RAGPipelineManager(
        db_path=r"D:\Graduation Project\Local\DB",
        model_name=embedding_model_name,
        query_transformer=query_transformer,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        k=5,
        retrive_method="similarity_search",
        query_processor=query_processor,
        crewagent=crewagent,
        hallucination=hallucination
    )

@st.cache_resource
def get_rag_manager():
    return initialize_rag_manager()

# Custom CSS for chat-like UI
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 10px 0;
    }
    .message {
        padding: 10px 15px;
        border-radius: 12px;
        max-width: 70%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }
    .assistant-message {
        background-color: #FFFFFF;
        align-self: flex-start;
        text-align: left;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True
)

def display_chat_history():
    """Render chat messages with distinct styles for user and assistant."""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["sender"] == "user":
            st.markdown(
                f'<div class="message user-message"><strong>👤 المستخدم:</strong> {msg["message"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message assistant-message"><strong>🤖 المساعد:</strong> {msg["message"]}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("Muffakir - Legal AI Assistant")
    st.write("مرحبا بك في المساعد القانوني الذكي!")
    
    # Initialize chat history if not already in session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Load RAG manager once
    rag_manager = get_rag_manager()
    
    # User input area
    user_input = st.text_input("اسأل سؤالاً قانونيًا:")

    if st.button("إرسال") and user_input:
        try:
            response = rag_manager.generate_answer(user_input)
            bot_answer = response.get("answer", "لم يتم الحصول على إجابة.")
        except Exception as e:
            bot_answer = f"حدث خطأ: {str(e)}"
        
        # Append messages to chat history
        st.session_state.chat_history.append({"sender": "user", "message": user_input})
        st.session_state.chat_history.append({"sender": "assistant", "message": bot_answer})
        
        # Store conversation in the RAG manager
        rag_manager.store_conversation(user_input, bot_answer)
    
    # Display conversation history with styled chat bubbles
    display_chat_history()

if __name__ == "__main__":
    main()
