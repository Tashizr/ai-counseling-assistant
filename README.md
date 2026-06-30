# AI Counseling Assistant

A locally-running AI counseling assistant for **education, research, and software engineering practice only**.

> **Disclaimer:** This is NOT a replacement for licensed mental health professionals. It cannot diagnose conditions, prescribe medication, or provide emergency care.

## Quick Start

```bash
# 1. Clone and enter the project
cd ai-counseling-assistant

# 2. Initialize the project
python init_project.py

# 3. Start Ollama (in a separate terminal)
ollama serve

# 4. Pull a model
ollama pull llama3.2

# 5. Run the application
streamlit run app.py
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design.

## Technology Stack

- **LLM:** Ollama (local)
- **Embeddings:** Sentence Transformers
- **Vector Store:** ChromaDB
- **Database:** SQLite
- **NLP:** spaCy
- **UI:** Streamlit

## Project Structure

```
├── config.py              # Centralized configuration
├── app.py                 # Streamlit entry point
├── logging_config/        # Structured logging
├── database/              # SQLite abstraction
├── prompts/               # Safety rules & system prompts
├── emotion_detection/     # Emotion classification
├── risk_detection/        # Risk level detection
├── memory/                # Short & long-term memory
├── rag/                   # Retrieval-Augmented Generation
├── preprocessing/         # Document cleaning & chunking
├── embeddings/            # Embedding generation
├── services/              # Orchestration layer
├── ui/                    # Streamlit pages & components
├── utils/                 # Shared utilities
└── tests/                 # Test suite
```

## Safety

This application implements multi-layer safety:

1. **Input screening** — crisis keyword detection
2. **System prompt rules** — non-negotiable safety constraints
3. **Output filtering** — post-generation safety checks
4. **Persistent safeguards** — identity disclosure, crisis resources

## License

For educational use only.
