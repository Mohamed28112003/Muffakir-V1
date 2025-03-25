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
from TextProcessor import *
from api_keys import api_keys_qroq, api_keys_together
from Reranker import *
from HallucinationsCheck import *
from QuizGeneration import *
from Search import Search


def initialize_rag_manager(db_path:str):
    embedding_model_name = "mohamed2811/Muffakir_Embedding"

    llm_provider = LLMProvider(
        provider_name="together",
        temperature=0,
        api_keys=api_keys_together,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
    )
    
    prompt_manager = PromptManager()
    query_transformer = QueryTransformer(llm_provider, prompt_manager, prompt="query_rewrite")
    query_processor = QueryDocumentProcessor(llm_provider, prompt_manager)
    hallucination = HallucinationsCheck(llm_provider, prompt_manager)





    return RAGPipelineManager(
        db_path=db_path,
        model_name=embedding_model_name,
        query_transformer=query_transformer,
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        k=5,
        retrive_method="similarity_search",
        query_processor=query_processor,
        hallucination=hallucination,
    )



@st.cache_resource
def get_rag_manager(db_path:str =r"D:\Graduation Project\Local\DB"):
    
    return initialize_rag_manager(db_path)

# Initialize Deep Search
def initialize_search():
    llm_provider = LLMProvider(
        provider_name="together",
        temperature=0,
        api_keys=api_keys_together,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
    )
    prompt_manager = PromptManager()
    params = {
        "maxDepth": 3,
        "timeLimit": 180,
        "maxUrls": 10
    }
    return Search(
        api_key="fc-3e3b5e78f7bf4f1eb755002c2afb0527",
        llm_provider=llm_provider,
        prompt_manager=prompt_manager,
        params=params
    )

@st.cache_resource
def get_search_instance():
    return initialize_search()

# Initialize Quiz Generator
def initialize_quiz():
    llm_provider = LLMProvider(
        provider_name="together",
        temperature=0,
        api_keys=api_keys_together,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
    )
    prompt_manager = PromptManager()
    rag_manager = get_rag_manager()
    doc = DocumentRetriever(rag_manager)
    return QuizGeneration(llm_provider, prompt_manager, retriever=doc)

@st.cache_resource
def get_quiz_instance():
    return initialize_quiz()

# Chat UI Styles
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
    """Display chat history"""
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
    st.write("🔹 مساعد قانوني ذكي يعتمد على الذكاء الاصطناعي في البحث والإجابة.")

    # Initialize session states
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "quiz_results" not in st.session_state:
        st.session_state.quiz_results = None

    # Load dependencies
    rag_manager = get_rag_manager()
    search_instance = get_search_instance()

    # User input
    user_input = st.text_input("📝 اسأل سؤالاً قانونيًا:")

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        send_button = st.button("💬 إرسال")
    with col2:
        search_button = st.button("🔎 بحث عميق")
    with col3:
        quiz_button = st.button("📝 توليد اختبار")

    # Quiz generation
    if quiz_button and user_input:
        try:
            quiz = get_quiz_instance()
            st.session_state.quiz_results = quiz.generate_quiz(query=user_input)
        except Exception as e:
            st.error(f"❌ خطأ أثناء إنشاء الاختبار: {str(e)}")

    # Quiz display and interaction
    if st.session_state.quiz_results and st.session_state.quiz_results["questions"]:
        st.subheader("📚 اختبار تفاعلي")
        
        # Add reset button
        if st.button("🗑️ مسح الاختبار"):
            st.session_state.quiz_results = None
            st.experimental_rerun()

        for i, (question, options, correct_answer, explanation) in enumerate(
            zip(
                st.session_state.quiz_results["questions"], 
                st.session_state.quiz_results["options"], 
                st.session_state.quiz_results["correct_answers"], 
                st.session_state.quiz_results["explanations"]
            )
        ):
            st.markdown(f"**سؤال {i+1}:** {question}")
            
            # Create radio buttons with persisted state
            option_letters = ["أ", "ب", "ج", "د"]
            selected_index = st.session_state.get(f"selected_option_{i}", None)
            user_answer = st.radio(
                "اختر الإجابة الصحيحة:",
                options,
                key=f"quiz_{i}_options",
                index=selected_index
            )
            
            # Store selection in session state
            if user_answer:
                st.session_state[f"selected_option_{i}"] = options.index(user_answer)
            
            # Show answer button
            if st.button(f"عرض الإجابة للسؤال {i+1}", key=f"show_answer_{i}"):
                try:
                    # Handle different answer formats
                    if correct_answer in option_letters:
                        correct_index = option_letters.index(correct_answer)
                    elif correct_answer.upper() in ['A', 'B', 'C', 'D']:
                        correct_index = ord(correct_answer.upper()) - ord('A')
                    elif len(correct_answer) == 1 and 'أ' <= correct_answer <= 'د':
                        arabic_map = {'أ': 0, 'ب': 1, 'ج': 2, 'د': 3}
                        correct_index = arabic_map.get(correct_answer, 0)
                    else:
                        try:
                            correct_index = int(correct_answer) - 1
                            if not 0 <= correct_index < len(options):
                                correct_index = 0
                        except ValueError:
                            correct_index = 0

                    if 0 <= correct_index < len(options):
                        st.success(f"**الإجابة الصحيحة:** {option_letters[correct_index]}. {options[correct_index]}")
                        st.info(f"**الشرح:** {explanation}")
                    else:
                        st.warning("مؤشر الإجابة خارج النطاق. الافتراضي للخيار الأول.")
                        st.success(f"**الإجابة الصحيحة:** {option_letters[0]}. {options[0]}")
                        st.info(f"**الشرح:** {explanation}")
                except Exception as e:
                    st.error(f"خطأ في عرض الإجابة: {str(e)}")
                    st.info(f"**الشرح:** {explanation}")
            
            st.markdown("---")

    # Handle chat responses
    if send_button and user_input:
        try:
            response = rag_manager.generate_answer(user_input)
            bot_answer = response.get("answer", "لم يتم العثور على إجابة.")
        except Exception as e:
            bot_answer = f"❌ خطأ: {str(e)}"
        
        # Store conversation
        st.session_state.chat_history.append({"sender": "user", "message": user_input})
        st.session_state.chat_history.append({"sender": "assistant", "message": bot_answer})
        rag_manager.store_conversation(user_input, bot_answer)
    
    # Handle deep search
    if search_button and user_input:
        with st.spinner("🔄 جاري تحسين الاستعلام وإجراء البحث..."):
            try:
                results = search_instance.deep_search(user_input)
                final_analysis = results["data"].get("finalAnalysis", "لا يوجد تحليل متاح.")
                sources = results["data"].get("sources", [])

                # Display results
                st.subheader("📌 التحليل النهائي:")
                st.write(final_analysis)

                st.subheader(f"🔗 المصادر ({len(sources)})")
                for idx, source in enumerate(sources, start=1):
                    st.write(f"{idx}. [{source['title']}]({source['url']})")
            except Exception as e:
                st.error(f"❌ خطأ أثناء البحث: {str(e)}")

    # Display chat history
    display_chat_history()

if __name__ == "__main__":
    main()