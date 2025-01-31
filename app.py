import streamlit as st
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
from api_keys import api_keys

# Set page configuration with dark theme
st.set_page_config(
    page_title="Muffakir",
    page_icon="🤖",
    layout="centered"
)

# Force dark theme
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #1E1E1E;
        }
        
        [data-testid="stHeader"] {
            background-color: #1E1E1E;
        }
        
        .stTextArea textarea {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border-color: #404040;
        }
        
        .stButton button {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: none;
        }
        
        .stButton button:hover {
            background-color: #5A5A5A;
        }
        
        .user-message {
            background-color: #2D2D2D;
            color: #FFFFFF;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border: 1px solid #404040;
        }
        
        .bot-message {
            background-color: #363636;
            color: #FFFFFF;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border: 1px solid #404040;
        }
        
        .source-document {
            background-color: #2D2D2D;
            color: #E0E0E0;
            padding: 0.5rem;
            border-radius: 0.3rem;
            border: 1px solid #404040;
            margin: 0.3rem 0;
            font-size: 0.9rem;
        }
        
        .metadata {
            background-color: #363636;
            color: #E0E0E0;
            padding: 0.5rem;
            border-left: 3px solid #7289DA;
            margin: 0.2rem 0;
            font-size: 0.85rem;
        }
        
        h1, h2, h3, h4, h5, h6, p {
            color: #FFFFFF !important;
        }
        
        .stMarkdown {
            color: #FFFFFF;
        }
        
        hr {
            border-color: #404040;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_rag_manager():
    """Initialize the RAG pipeline manager with all necessary components"""
    embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    llm_provider = LLMProvider(api_keys=api_keys, model="llama-3.3-70b-versatile")
    prompt_manager = PromptManager()
    text_processor = TextProcessor()
    query_generator = QueryGenerator(llm_provider, prompt_manager)
    summary_chunker = SummaryChunker(llm_provider, prompt_manager)
    query_transformer = QueryTransformer(llm_provider, prompt_manager)
    
    return RAGPipelineManager(
        db_path="D:\Graduation Project\Local\DB_FINAL\content\DB_FINAL",
        model_name=embedding_model_name,
        query_transformer=query_transformer,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        k=3,
        retrive_method="contextual"
    )

# Main title with custom styling
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'> Muffakir 🤖</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize RAG manager
@st.cache_resource
def get_rag_manager():
    return initialize_rag_manager()

rag_manager = get_rag_manager()

# Chat interface
with st.container():
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 Muffakir :  {message["answer"]}</div>', unsafe_allow_html=True)
            if "sources" in message:
                st.markdown("<p style='color: #E0E0E0;'><strong>Source Documents and Metadata:</strong></p>", unsafe_allow_html=True)
                for i, (doc, metadata) in enumerate(zip(message["sources"], message.get("book", [])), 1):
                    st.markdown(f'<div class="source-document">Document {i}:<br>{doc}</div>', unsafe_allow_html=True)
                    if metadata:
                        st.markdown(f'<div class="metadata">📚 Source Metadata:<br>{metadata}</div>', unsafe_allow_html=True)
            st.markdown("---")

# User input
user_input = st.text_area("Ask your legal question:", height=100, key="user_input")
submit_button = st.button("Submit Question")

# Process user input
if submit_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Show loading spinner while processing
    with st.spinner("Generating answer..."):
        try:
            # Generate response
            response = rag_manager.generate_answer(user_input)
            
            # Add bot response to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "answer": response["answer"],
                "sources": response["retrieved_documents"],
                "book": response["source_metadata"]
            })
            
            # Rerun to update the display
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'><em>Built with Streamlit and RAG Pipeline</em></p>", unsafe_allow_html=True)