# AI Counseling Assistant — Architecture & Development Plan

## 1. Project Overview

A modular, production-quality, locally-running AI Counseling Assistant for **education, research, and software engineering practice only**. Powered by Ollama, with RAG, emotion detection, risk detection, memory, and a Streamlit UI.

**Not a replacement for licensed mental health professionals.**

---

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| LLM | Ollama (local) |
| Embeddings | Sentence Transformers |
| Vector Store | ChromaDB (replaces FAISS for easier persistence) |
| Database | SQLite |
| Web UI | Streamlit |
| NLP | spaCy |
| ML | scikit-learn, NumPy, Pandas |
| Testing | pytest |
| VCS | Git |

---

## 3. Module Dependency Graph

```
config.py (foundation — no deps)
    │
    ├── database/        (SQLite abstraction)
    │       │
    │       ├── memory/  (short-term + long-term memory, depends on database/)
    │       │
    │       └── mood/    (mood tracking, depends on database/)
    │
    ├── preprocessing/   (document cleaning, depends on config)
    │       │
    │       └── embeddings/ (vector generation, depends on preprocessing/)
    │               │
    │               └── rag/ (retrieval + generation, depends on embeddings/)
    │
    ├── emotion_detection/  (standalone ML module)
    │
    ├── risk_detection/     (standalone ML module, depends on emotion_detection/)
    │
    ├── prompts/            (template management, depends on config)
    │
    ├── services/           (orchestration layer — ties everything together)
    │       │
    │       ├── conversation_engine.py  (main brain)
    │       ├── safety_service.py       (risk + safety rules)
    │       └── session_manager.py      (session lifecycle)
    │
    ├── ui/                 (Streamlit pages)
    │
    └── tests/
```

---

## 4. Development Phases

### Phase 1: Foundation (Week 1)
**Goal:** Project scaffolding, config, database, safety guardrails

| Module | Purpose | Priority |
|---|---|---|
| `config.py` | Centralized configuration | Critical |
| `database/` | SQLite abstraction layer | Critical |
| `logging/` | Structured logging setup | Critical |
| `prompts/` | System prompts with safety rules | Critical |

### Phase 2: Knowledge Pipeline (Week 2)
**Goal:** RAG pipeline — document ingestion through retrieval

| Module | Purpose | Priority |
|---|---|---|
| `preprocessing/` | Document cleaning, chunking | High |
| `embeddings/` | Sentence transformer integration | High |
| `rag/` | ChromaDB storage + retrieval | High |
| `datasets/` | Sample educational documents | High |

### Phase 3: Intelligence (Week 3)
**Goal:** Emotion detection, risk detection, memory

| Module | Purpose | Priority |
|---|---|---|
| `emotion_detection/` | Multi-label emotion classifier | High |
| `risk_detection/` | Risk level classification | Critical |
| `memory/` | Short-term + long-term memory | High |

### Phase 4: Conversation Engine (Week 4)
**Goal:** Main orchestration — ties all modules together

| Module | Purpose | Priority |
|---|---|---|
| `services/` | Conversation engine, safety service | Critical |
| `services/` | Session manager | High |

### Phase 5: Interface (Week 5)
**Goal:** Streamlit UI — chat, dashboard, settings

| Module | Purpose | Priority |
|---|---|---|
| `ui/` | Chat interface | High |
| `ui/` | Mood tracker, session summaries | Medium |
| `ui/` | Settings, debug mode | Medium |

### Phase 6: Polish (Week 6)
**Goal:** Testing, documentation, optimization

| Module | Purpose | Priority |
|---|---|---|
| `tests/` | Unit + integration tests | High |
| `docs/` | User + developer documentation | Medium |
| Performance | Caching, optimization | Medium |

---

## 5. Data Flow

```
User Input
    │
    ▼
┌─────────────────┐
│  Safety Guard    │ ◄── risk_detection/ + hardcoded rules
│  (pre-check)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Emotion Detect   │ ◄── emotion_detection/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Memory Retrieve  │ ◄── memory/ (SQLite)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RAG Retrieval    │ ◄── rag/ (ChromaDB + Ollama embeddings)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Prompt Assembly  │ ◄── prompts/ (templates + context)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ollama Generate  │ ◄── local LLM
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Safety Guard     │ ◄── post-generation check
│ (post-check)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Memory Store     │ ◄── memory/ (conversation + mood)
└────────┬────────┘
         │
         ▼
     Response to User
```

---

## 6. Safety Architecture

Safety is enforced at THREE layers:

### Layer 1: Input Pre-screening
- Keyword/regex blocklist for dangerous content
- Crisis keyword detection triggers immediate resource display
- Emotional intensity measurement

### Layer 2: Prompt Engineering
- System prompt contains hard safety rules
- Rules are non-negotiable and placed at highest priority
- Model is instructed to refuse harmful requests regardless of context

### Layer 3: Output Filtering
- Post-generation scan for policy violations
- Verify disclaimer is included when appropriate
- Check for unauthorized claims (diagnosis, medication advice)

### Layer 4: Persistent Safeguards
- Every conversation starts with AI identity disclosure
- Crisis resources shown when risk >= Moderate
- Session data encrypted at rest (future enhancement)

---

## 7. Configuration Strategy

All configurable values live in `config.py` and `.env`:

- `OLLAMA_BASE_URL` — Ollama server address
- `OLLAMA_MODEL` — default model name
- `EMBEDDING_MODEL` — sentence transformer model
- `CHROMA_PERSIST_DIR` — vector store location
- `DATABASE_PATH` — SQLite file location
- `LOG_LEVEL` — logging verbosity
- `MAX_CONTEXT_LENGTH` — token limit for LLM context
- `RISK_THRESHOLD` — risk level that triggers safety response
- `ENABLE_DEBUG` — debug mode flag

---

## 8. File Structure

```
ai-counseling-assistant/
│
├── app.py                      # Streamlit entry point
├── config.py                   # Central configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment variable template
├── .gitignore
├── ARCHITECTURE.md             # This file
├── README.md                   # User-facing documentation
│
├── datasets/                   # Educational documents for RAG
│   ├── raw/                    # Unprocessed source files
│   ├── processed/              # Cleaned and chunked data
│   └── sample_data.json        # Demo data for testing
│
├── preprocessing/
│   ├── __init__.py
│   ├── cleaner.py              # Text cleaning and normalization
│   ├── chunker.py              # Semantic text splitting
│   └── loader.py               # Document loading (PDF, TXT, JSON)
│
├── embeddings/
│   ├── __init__.py
│   ├── generator.py            # Embedding generation
│   └── cache.py                # Embedding cache
│
├── rag/
│   ├── __init__.py
│   ├── vector_store.py         # ChromaDB interface
│   ├── retriever.py            # Query and retrieval logic
│   └── generator.py            # Context-augmented generation
│
├── emotion_detection/
│   ├── __init__.py
│   ├── detector.py             # Emotion classification
│   ├── models.py               # Emotion data classes
│   └── keywords.py             # Emotion keyword dictionaries
│
├── risk_detection/
│   ├── __init__.py
│   ├── detector.py             # Risk level classification
│   ├── models.py               # Risk data classes
│   ├── signals.py              # Risk signal extraction
│   └── crisis_resources.py     # Emergency resources by country
│
├── memory/
│   ├── __init__.py
│   ├── short_term.py           # Current session memory
│   ├── long_term.py            # Persistent memory (SQLite)
│   ├── summarizer.py           # Conversation summarization
│   └── models.py               # Memory data classes
│
├── prompts/
│   ├── __init__.py
│   ├── system_prompt.py        # Core system prompt with safety rules
│   ├── templates.py            # Response templates
│   └── safety_rules.py         # Non-negotiable safety constraints
│
├── database/
│   ├── __init__.py
│   ├── connection.py           # SQLite connection manager
│   ├── models.py               # Database schema definitions
│   └── migrations.py           # Schema versioning
│
├── services/
│   ├── __init__.py
│   ├── conversation_engine.py  # Main orchestration brain
│   ├── safety_service.py       # Safety checking service
│   └── session_manager.py      # Session lifecycle management
│
├── ui/
│   ├── __init__.py
│   ├── pages/
│   │   ├── chat.py             # Main chat interface
│   │   ├── mood_tracker.py     # Mood visualization
│   │   ├── session_history.py  # Past conversations
│   │   ├── memory_viewer.py    # Memory inspection
│   │   ├── knowledge_base.py   # KB stats and management
│   │   ├── settings.py         # Configuration UI
│   │   └── debug.py            # Developer debug panel
│   ├── components/
│   │   ├── sidebar.py          # Navigation sidebar
│   │   ├── chat_bubble.py      # Message display component
│   │   └── mood_chart.py       # Mood visualization charts
│   └── styles.py               # Custom CSS styling
│
├── utils/
│   ├── __init__.py
│   ├── text_utils.py           # Text processing helpers
│   ├── time_utils.py           # Time/date helpers
│   └── validators.py           # Input validation
│
├── logging_config/
│   ├── __init__.py
│   └── setup.py                # Logging configuration
│
├── models/                     # Downloaded/pre-trained models
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_emotion_detection/
│   ├── test_risk_detection/
│   ├── test_memory/
│   ├── test_rag/
│   ├── test_services/
│   └── test_preprocessing/
│
└── docs/
    ├── user_guide.md
    ├── developer_guide.md
    └── api_reference.md
```

---

## 9. Implementation Order

Build in this exact sequence to minimize rework:

```
1. config.py                    ← Foundation
2. logging_config/setup.py      ← Foundation
3. database/connection.py       ← Foundation
4. database/models.py           ← Foundation
5. prompts/safety_rules.py      ← Safety first
6. prompts/system_prompt.py     ← Safety first
7. emotion_detection/           ← Independent module
8. risk_detection/              ← Depends on emotion_detection
9. preprocessing/               ← Independent module
10. embeddings/                 ← Depends on preprocessing
11. rag/                        ← Depends on embeddings
12. memory/                     ← Depends on database
13. services/safety_service.py  ← Ties safety together
14. services/conversation_engine.py ← Main brain
15. services/session_manager.py ← Session lifecycle
16. ui/                         ← Final layer
17. app.py                      ← Entry point
18. tests/                      ← Throughout, but bulk at end
```

---

## 10. Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Vector store | ChromaDB over FAISS | Built-in persistence, easier API, metadata filtering |
| NLP | spaCy over NLTK | Faster, production-ready, better pipeline support |
| Database | SQLite | Local-first, zero config, easily replaceable later |
| UI | Streamlit | Fast development, Python-native, good chat support |
| Memory abstraction | Interface-based | Easy to swap SQLite for PostgreSQL later |
| Safety | Multi-layered | No single point of failure for safety rules |
| Config | .env + config.py | Separates secrets from code |

---

## 11. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Model gives harmful advice | High | Multi-layer safety, output filtering, hardcoded refusals |
| False negative in risk detection | High | Conservative thresholds, keyword fallbacks, human escalation |
| PII stored in logs | Medium | Structured logging, log rotation, no user text in logs |
| RAG returns inappropriate content | Medium | Curated dataset only, content filtering |
| Ollama server unavailable | Low | Graceful degradation, clear error messages |
| SQLite concurrent access | Low | WAL mode, connection pooling |
