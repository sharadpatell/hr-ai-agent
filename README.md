# HR AI Agent

A sophisticated AI-powered assistant for HR interview preparation, built with LangChain, ChromaDB, and Ollama. This agent retrieves and answers questions based on scraped HR interview data from various sources, using advanced retrieval techniques like MMR and BM25 for accurate, diverse responses.

## Features

- **Intelligent Retrieval**: Combines semantic (vector) and keyword-based (BM25) search for precise, relevant answers.
- **Source Filtering**: Query-specific filtering to pull from targeted sources (e.g., "questions from Naukri").
- **Diverse Responses**: Uses Maximal Marginal Relevance (MMR) to avoid repetitive chunks.
- **Math Support**: Handles basic calculations.
- **Streamlit UI**: User-friendly web interface for easy interaction.
- **Extensible**: Easily add more data sources or integrate APIs.

## What We Built

This project demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline:

1. **Data Ingestion**: Scrapes HR interview Q&A from websites (e.g., Naukri, InterviewBit, GeeksforGeeks) and stores raw text.
2. **Embedding & Chunking**: Splits text into 1000-character chunks with 200-character overlap, embeds using Ollama's nomic-embed-text, and stores in ChromaDB vector database.
3. **Retrieval**: Advanced hybrid search (BM25 + MMR) with source filtering for targeted queries.
4. **Generation**: Uses Ollama LLM (e.g., Llama 3.2) to generate answers strictly from retrieved context.
5. **Decision Logic**: Routes queries to retrieval, math, or general responses.
6. **UI**: Streamlit app with chat history and debug logs.

Improvements include deduplication, better chunking, and model optimization for reliable extraction.

## Prerequisites

- **Python 3.8+**: Download from [python.org](https://www.python.org/).
- **Ollama**: Required for local LLM and embeddings.
  - Install from [ollama.ai](https://ollama.ai/).
  - Pull models: `ollama pull llama3.2:3b` (for generation) and `ollama pull nomic-embed-text` (for embeddings).
- **Git**: For cloning/version control.

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/hr-ai-agent.git
   cd hr-ai-agent
   ```

2. **Set Up Virtual Environment**:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Prepare Data** (Optional: Skip if using pre-scraped data):
   - Run scraper: `python ingestion/scraper.py`
   - Run embedder: `python ingestion/embedder.py`

5. **Ensure Ollama Models**:
   - Start Ollama: `ollama serve`
   - Pull models if not done: `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`

## Usage

1. **Run the App**:
   ```
   streamlit run app/app.py
   ```
   - Open http://localhost:8501 in your browser.

2. **Interact**:
   - Ask HR-related questions, e.g., "Tips for answering 'Tell me about yourself'".
   - For source-specific: "HR questions from InterviewBit".
   - Math: "Calculate 5 + 3".

3. **Debug**: Use the sidebar toggle for logs.



## Project Structure

```
hr-ai-agent/
├── agent/              # Core logic (retriever, LLM, agent)
├── app/                # Streamlit UI
├── ingestion/          # Scraper and embedder
├── data/               # Raw scraped data
├── requirements.txt    # Dependencies
├── README.md           # This file
└── .gitignore          # Ignore logs, cache, vector DB
```

## Contributing

1. Fork the repo.

## License

MIT License. See LICENSE for details.

## Troubleshooting

- **Model Not Found**: Run `ollama pull <model>`.
- **Import Errors**: Ensure virtual env is activated and dependencies installed.
- **No Responses**: Check Ollama is running and vector DB exists.

For issues, open a GitHub issue.