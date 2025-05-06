import pytest
from init import initialize_rag_manager

@pytest.fixture(scope="module")
def real_rag_manager():
    # تهيئة مدير RAG مع بيانات حقيقية
    manager = initialize_rag_manager()
    yield manager
    # تنظيف بعد الانتهاء (اختياري)
    #manager.db_manager.vector_store.delete_collection()

def test_real_history_processing(real_rag_manager):
    # اختبار تفاعل حقيقي مع التاريخ
    real_rag_manager.store_conversation(
        "ما هو القانون الجنائي؟",
        "القانون الذي ينظم الجرائم والعقوبات."
    )
    
    response = real_rag_manager.generate_answer("ما هو القصد الجنائي؟")
    assert "القصد الجنائي" in response["answer"]
    assert len(response["retrieved_documents"]) > 0



