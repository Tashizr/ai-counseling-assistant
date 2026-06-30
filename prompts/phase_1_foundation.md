# Phase 1: Foundation — Mimo 2.5 Implementation Prompt

## Context

You are implementing Phase 1 of an AI Counseling Assistant. This is a locally-running Python application using Ollama, ChromaDB, SQLite, and Streamlit. You are building the foundational modules: configuration, logging, database, and safety prompts.

**Project root:** `C:\Users\Crystal\Desktop\ai-counseling-assistant`

**Important:** This project is for education, research, and software engineering practice only. It must never claim to be a licensed therapist.

---

## Task 1: Project Root Files

### File: `requirements.txt`

Create with these exact dependencies:

```
# Core
streamlit>=1.31.0
python-dotenv>=1.0.0

# LLM
ollama>=0.4.0

# Embeddings & Vector Store
sentence-transformers>=2.3.0
chromadb>=0.4.22

# NLP
spacy>=3.7.0

# ML
scikit-learn>=1.4.0
numpy>=1.26.0
pandas>=2.2.0

# Database
# (sqlite3 is built-in)

# Testing
pytest>=8.0.0
pytest-cov>=4.1.0

# Utilities
requests>=2.31.0
```

### File: `.gitignore`

```
__pycache__/
*.pyc
.env
*.db
chroma_db/
models/
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
```

### File: `.env.example`

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./chroma_db
DATABASE_PATH=./data/counseling.db
LOG_LEVEL=INFO
ENABLE_DEBUG=false
```

---

## Task 2: `config.py` (Project Root)

Create a centralized configuration module.

```python
"""
Centralized configuration for AI Counseling Assistant.
Loads from .env file with sensible defaults.
"""
```

### Requirements:

1. Use `python-dotenv` to load `.env`
2. Define a `Settings` dataclass with all configuration fields
3. Create a module-level `settings` singleton
4. All values must be configurable, none hardcoded
5. Include type hints on every field
6. Include docstrings on the class and each field

### Settings Fields:

```python
@dataclass(frozen=True)
class Settings:
    # Ollama
    ollama_base_url: str          # default: "http://localhost:11434"
    ollama_model: str             # default: "llama3.2"
    ollama_timeout: int           # default: 120 (seconds)

    # Embeddings
    embedding_model: str          # default: "all-MiniLM-L6-v2"
    embedding_dimension: int      # default: 384

    # ChromaDB
    chroma_persist_dir: str       # default: "./chroma_db"
    chroma_collection: str        # default: "counseling_knowledge"

    # Database
    database_path: str            # default: "./data/counseling.db"

    # Logging
    log_level: str                # default: "INFO"
    log_dir: str                  # default: "./logs"
    max_log_size_mb: int          # default: 10
    log_backup_count: int         # default: 5

    # Conversation
    max_context_messages: int     # default: 20
    max_response_tokens: int      # default: 512
    temperature: float            # default: 0.7
    top_p: float                  # default: 0.9

    # Safety
    risk_threshold: str           # default: "moderate" (low|moderate|high|critical)
    enable_safety_filters: bool   # default: True
    crisis_keywords_file: str     # default: "./prompts/crisis_keywords.json"

    # RAG
    rag_top_k: int                # default: 5
    rag_similarity_threshold: float  # default: 0.3

    # Memory
    short_term_max_messages: int  # default: 50
    long_term_summary_interval: int  # default: 10 (messages)

    # UI
    enable_debug: bool            # default: False
    app_title: str                # default: "AI Counseling Assistant"
    app_icon: str                 # default: "🧠"
    theme_primary: str            # default: "#4A90D9"
```

### Module-level access:

```python
settings = Settings()

# Convenience accessors
def get_settings() -> Settings:
    """Return the global settings instance."""
    return settings
```

### Validation:

- `Settings.__post_init__` should validate:
  - `temperature` between 0.0 and 2.0
  - `top_p` between 0.0 and 1.0
  - `risk_threshold` in ["low", "moderate", "high", "critical"]
  - `log_level` in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
  - Raise `ValueError` with clear message on invalid values

### Error Handling:

- If `.env` file is missing, use defaults silently (log a warning)
- If env vars have wrong types, raise `ValueError` with the variable name

---

## Task 3: `logging_config/` Module

### File: `logging_config/__init__.py`

Export `setup_logging`.

### File: `logging_config/setup.py`

```python
"""
Structured logging configuration for the AI Counseling Assistant.
"""
```

### Requirements:

1. Function `setup_logging(log_level: str, log_dir: str, max_size_mb: int, backup_count: int) -> logging.Logger`
2. Create `logs/` directory if it doesn't exist
3. Configure two handlers:
   - **ConsoleHandler**: Human-readable format, colored output
   - **FileHandler**: JSON-structured format for machine parsing
4. Log format for console: `%(asctime)s | %(levelname)-8s | %(name)s | %(message)s`
5. Log format for file: JSON with timestamp, level, logger, message, module, function, line
6. Set up root logger and return a module-specific logger
7. **Privacy rule**: Never log user message content at INFO level or above. User text must only appear in DEBUG logs, and even then, truncate to 100 chars.
8. Create a helper `get_logger(name: str) -> logging.Logger` that returns a named logger

### File Structure:

```
logging_config/
├── __init__.py
└── setup.py
```

---

## Task 4: `database/` Module

### File: `database/__init__.py`

Export `DatabaseManager` and `get_database`.

### File: `database/connection.py`

```python
"""
SQLite connection manager with WAL mode and connection pooling.
"""
```

### Requirements:

1. Class `DatabaseManager`:
   - `__init__(self, db_path: str)` — creates parent directories if needed
   - `get_connection(self) -> sqlite3.Connection` — returns connection with WAL mode, foreign keys enabled, row factory set to `sqlite3.Row`
   - Context manager support: `__enter__` and `__exit__`
   - `execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor`
   - `fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]`
   - `fetch_all(self, query: str, params: tuple = ()) -> list[dict]`
   - `close(self)` — close all connections
2. Use `threading.local()` for thread-safe connection storage
3. WAL mode enabled for concurrent reads
4. Foreign keys always enabled
5. Connection timeout of 10 seconds
6. Log all queries at DEBUG level (never log user data in queries)

### File: `database/models.py`

```python
"""
Database schema definitions and migration management.
"""
```

### Requirements:

1. Define schema as SQL strings in a dict:
   - `conversations` table: id (TEXT PRIMARY KEY), user_id, started_at, ended_at, summary, mood_start, mood_end, risk_level_max, created_at
   - `messages` table: id, conversation_id (FK), role (user/assistant), content, emotion_primary, emotion_confidence, risk_level, timestamp
   - `user_profiles` table: id, name, preferences (JSON), created_at, updated_at
   - `mood_entries` table: id, user_id, conversation_id (FK), mood_score (1-10), emotions (JSON), notes, timestamp
   - `memory_entries` table: id, user_id, category (short_term/long_term), content, importance (1-5), created_at, accessed_at, expires_at

2. Function `initialize_database(db: DatabaseManager) -> None`:
   - Create all tables if they don't exist
   - Create indexes on foreign keys and timestamps
   - Log initialization

3. Function `run_migrations(db: DatabaseManager) -> None`:
   - Simple version tracking in a `schema_version` table
   - Future-proof for schema changes

### File: `database/migrations.py`

```python
"""
Database migration system for schema versioning.
"""
```

### Requirements:

1. Class `Migration` with `version: int`, `description: str`, `up_sql: str`, `down_sql: str`
2. A registry of migrations as a list
3. Function `get_current_version(db: DatabaseManager) -> int`
4. Function `migrate_to_latest(db: DatabaseManager) -> None`
5. Start with version 1 as the initial schema

---

## Task 5: `prompts/` Module

**CRITICAL: This module contains safety-critical content. Every response from the AI must follow these rules.**

### File: `prompts/__init__.py`

Export `get_system_prompt`, `get_safety_rules`, `CRISIS_RESOURCES`.

### File: `prompts/safety_rules.py`

```python
"""
Non-negotiable safety rules for the AI Counseling Assistant.
These rules take highest priority in all interactions.
"""
```

### Requirements:

1. Constant `SAFETY_RULES` — a list of strings, each a rule:

```python
SAFETY_RULES = [
    "IDENTITY: You are an AI counseling assistant, NOT a licensed therapist, counselor, psychologist, or psychiatrist. Always be honest about this.",
    "NO DIAGNOSIS: Never diagnose mental health conditions. Never suggest medications. Never interpret clinical assessments.",
    "CRISIS RESPONSE: If the user expresses suicidal thoughts, self-harm intent, or intent to harm others, immediately provide crisis resources and encourage them to contact emergency services or a crisis hotline. Continue responding with empathy but do not attempt to handle crisis alone.",
    "NO ENCOURAGEMENT OF HARM: Never encourage, validate, or provide instructions for self-harm, suicide, or harming others under any circumstances.",
    "EMOTIONAL MANIPULATION: Never manipulate users emotionally. Never guilt-trip. Never use fear-based persuasion.",
    "HUMANITY: Never pretend to be human. Always be transparent that you are an AI.",
    "PROFESSIONAL BOUNDARY: Encourage users to seek professional help when appropriate. You are a supportive tool, not a replacement for professional care.",
    "PRIVACY: Never ask for or store personally identifiable information beyond first name. Never share user data.",
    "LIMITATIONS: Acknowledge your limitations honestly when asked. You are not a replacement for professional mental health services.",
    "AFFIRMATION WITHOUT REINFORCEMENT: Validate feelings without reinforcing harmful beliefs or dangerous behaviors.",
    "CULTURAL SENSITIVITY: Be respectful of all cultural backgrounds, identities, and experiences.",
    "NO MEDICAL ADVICE: Never provide medical advice, including about medications, supplements, or treatments.",
]
```

2. Function `get_safety_rules() -> list[str]`: returns the safety rules

3. Constant `CRISIS_RESOURCES` — a dict mapping country codes to crisis resource info:

```python
CRISIS_RESOURCES = {
    "US": {
        "name": "988 Suicide & Crisis Lifeline",
        "phone": "988",
        "text": "Text HOME to 741741",
        "web": "https://988lifeline.org",
    },
    "UK": {
        "name": "Samaritans",
        "phone": "116 123",
        "text": "Text SHOUT to 85258",
        "web": "https://www.samaritans.org",
    },
    "CA": {
        "name": "Talk Suicide Canada",
        "phone": "1-833-456-4566",
        "text": "Text 45645",
        "web": "https://talksuicide.ca",
    },
    "AU": {
        "name": "Lifeline Australia",
        "phone": "13 11 14",
        "text": "Text 0477 13 11 14",
        "web": "https://www.lifeline.org.au",
    },
    "IN": {
        "name": "Vandrevala Foundation",
        "phone": "1860-2662-345",
        "web": "https://www.vandrevalafoundation.com",
    },
    "DEFAULT": {
        "name": "International Association for Suicide Prevention",
        "web": "https://www.iasp.info/resources/Crisis_Centres/",
    },
}
```

### File: `prompts/templates.py`

```python
"""
Response templates for consistent AI behavior.
"""
```

### Requirements:

1. Constant `IDENTITY_DISCLAIMER`:

```python
IDENTITY_DISCLAIMER = (
    "Before we continue, I want to be transparent: I'm an AI counseling assistant, "
    "not a licensed therapist or mental health professional. I'm here to provide "
    "support and listen, but I cannot diagnose conditions, prescribe medication, "
    "or replace professional care. If you're in crisis, please reach out to a "
    "crisis hotline or emergency services."
)
```

2. Constant `CRISIS_RESPONSE_TEMPLATE`:

```python
CRISIS_RESPONSE_TEMPLATE = (
    "I hear you, and I want you to know that what you're feeling matters. "
    "What you're describing sounds serious, and I want to make sure you get "
    "the support you deserve.\n\n"
    "Please consider reaching out to:\n"
    "**{resource_name}**: {resource_contact}\n"
    "Web: {resource_web}\n\n"
    "You don't have to go through this alone. Would you like to talk more "
    "about what you're experiencing while also reaching out for professional support?"
)
```

3. Constant `SUMMARY_TEMPLATE` — template for conversation summaries:

```python
SUMMARY_TEMPLATE = (
    "Summarize this counseling conversation in 3-5 sentences. "
    "Focus on: main topics discussed, emotions expressed, coping strategies mentioned, "
    "and any goals or action items. Be empathetic and factual. "
    "Do not include diagnostic language."
)
```

4. Function `build_system_prompt(
    safety_rules: list[str],
    context: str,
    memory_context: str,
    rag_context: str,
    user_name: Optional[str],
    emotion: Optional[str],
    risk_level: str,
) -> str`:

   This function assembles the full system prompt:

   ```
   You are an AI counseling assistant... [identity]
   
   ## Safety Rules
   [each rule as numbered item]
   
   ## Current Context
   - User's name: {user_name or "Not provided"}
   - Detected emotion: {emotion or "Unknown"}
   - Risk level: {risk_level}
   
   ## Relevant Knowledge
   [RAG retrieved passages, or "No relevant passages found."]
   
   ## Conversation Memory
   [Memory context, or "No prior context."]
   
   ## Instructions
   - Respond with empathy and active listening
   - Ask meaningful follow-up questions
   - Reflect the user's emotions back to them
   - Use the retrieved knowledge naturally, not robotically
   - If risk level is moderate or above, include gentle encouragement to seek support
   - Never violate the safety rules above
   ```

### File: `prompts/system_prompt.py`

```python
"""
Core system prompt construction for the AI Counseling Assistant.
"""
```

### Requirements:

1. Function `get_system_prompt(
    user_name: Optional[str] = None,
    emotion: Optional[str] = None,
    risk_level: str = "low",
    rag_context: str = "",
    memory_context: str = "",
    conversation_context: str = "",
) -> str`

2. This calls `build_system_prompt` from templates.py with the assembled data

3. Must include the identity disclaimer at the top

4. Must include all safety rules

5. Must adapt tone based on risk level:
   - low: warm, supportive
   - moderate: warm, gently encouraging professional support
   - high: calm, focused on safety, strongly encouraging professional help
   - critical: immediate crisis response, prioritizing safety resources

---

## Task 6: Project Initialization Script

### File: `init_project.py`

A script that:

1. Creates all required directories:
   - `datasets/raw/`, `datasets/processed/`
   - `data/`
   - `logs/`
   - `chroma_db/`
   - `models/`
   - All package directories with `__init__.py`

2. Runs `pip install -r requirements.txt`

3. Downloads the spaCy model: `python -m spacy download en_core_web_sm`

4. Initializes the database with `initialize_database`

5. Creates `.env` from `.env.example` if it doesn't exist

6. Prints a success message with next steps

---

## Cross-Cutting Requirements

For ALL files in this phase:

1. **Type hints** on every function signature and return type
2. **Docstrings** on every module, class, and public function (Google style)
3. **PEP 8** compliance
4. **Error handling** — no bare `except:` clauses; catch specific exceptions
5. **Logging** — use `logging` module; log initialization, key operations, and errors; never log user data at INFO+
6. **No hardcoded values** — all configurable values come from `config.py`
7. **`__all__`** exports in every `__init__.py`
8. **No unused imports**
9. **Constants in UPPER_SNAKE_CASE**
10. **Classes in PascalCase**
11. **Functions in snake_case**
12. **Private methods prefixed with underscore**

---

## Verification Checklist

After implementing, verify:

- [ ] All files created in correct locations
- [ ] `config.py` loads from `.env` with defaults
- [ ] `config.py` validates settings on construction
- [ ] Logging writes to both console and file
- [ ] Database creates tables on initialization
- [ ] Safety rules are comprehensive and non-bypassable
- [ ] System prompt includes identity disclaimer
- [ ] Crisis resources are included for multiple countries
- [ ] All type hints present
- [ ] All docstrings present
- [ ] No bare except clauses
- [ ] No hardcoded values outside config
