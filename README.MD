# Muffakir 🤖

A Streamlit-based chatbot application that uses RAG (Retrieval-Augmented Generation) to answer legal questions in Arabic. The application provides intelligent responses with source documentation and metadata.




## Installation

1. Clone the repository or download the source code:
```bash
git clone <repository-url>
```

2. Create a environment:
```bash
 conda create -n muffakir python=3.11
```

3. Activate the environment:
```bash
conda activate muffakir
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt

```


## Project Structure

Ensure you have the following files in your project directory:
```
legal-assistant-chatbot/
├── app.py                    # Main Streamlit application
├── api_keys.py              # API keys configuration
├── AnswerGenerator.py       # Answer generation module
├── ChromaDBManager.py       # ChromaDB management module
├── DocumentRetriever.py     # Document retrieval module
├── EmbeddingProvider.py     # Embedding generation module
├── LLMProvider.py           # Language model provider
├── PromptManager.py         # Prompt management module
├── QueryGenerator.py        # Query generation module
├── QueryTransformer.py      # Query transformation module
├── RAGGenerationPipeline.py # RAG pipeline module
├── RAGPipelineManager.py    # RAG pipeline management
├── RetrieveMethods.py       # Retrieval methods module
├── SummaryChunker.py        # Text chunking module
└── TextProcessor.py         # Text processing module
└── Reranker.py              # Reranker module

```

## Configuration

1. Update the database path in `app.py`:
```python
db_path = "path/to/your/database"
```

## Running the Application

1. Make sure you're in the project directory and your  environment is activated.

2. Run the Streamlit application:
```bash
python -m streamlit run app.py
or 
streamlit run app.py
```

