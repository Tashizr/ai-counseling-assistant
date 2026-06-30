"""
Project initialization script for the AI Counseling Assistant.

Creates required directories, installs dependencies, downloads models,
and initializes the database. Run once after cloning.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

DIRECTORIES = [
    "datasets/raw",
    "datasets/processed",
    "data",
    "logs",
    "chroma_db",
    "models",
]

PACKAGES = [
    "logging_config",
    "database",
    "prompts",
    "emotion_detection",
    "risk_detection",
    "memory",
    "preprocessing",
    "embeddings",
    "rag",
    "services",
    "ui",
    "ui/pages",
    "ui/components",
    "utils",
    "tests",
]


def create_directories() -> None:
    """Create all required project directories."""
    print("Creating directories...")
    for directory in DIRECTORIES + PACKAGES:
        path = PROJECT_ROOT / directory
        path.mkdir(parents=True, exist_ok=True)
        init_file = path / "__init__.py"
        if directory in PACKAGES and not init_file.exists():
            init_file.write_text(f'"""Package: {directory}"""\n')
        print(f"  [OK] {directory}")
    print()


def install_dependencies() -> None:
    """Install Python dependencies from requirements.txt."""
    print("Installing dependencies...")
    requirements = PROJECT_ROOT / "requirements.txt"
    if requirements.exists():
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("  [OK] Dependencies installed")
        else:
            print(f"  [WARN] pip install had issues: {result.stderr[:200]}")
    else:
        print("  [SKIP] requirements.txt not found")
    print()


def download_spacy_model() -> None:
    """Download the spaCy English language model."""
    print("Downloading spaCy model...")
    result = subprocess.run(
        [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("  [OK] en_core_web_sm downloaded")
    else:
        print(f"  [WARN] spaCy download had issues: {result.stderr[:200]}")
    print()


def setup_env() -> None:
    """Copy .env.example to .env if .env doesn't exist."""
    env_example = PROJECT_ROOT / ".env.example"
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        print("  [SKIP] .env already exists")
    elif env_example.exists():
        shutil.copy(env_example, env_file)
        print("  [OK] Created .env from .env.example")
    else:
        print("  [SKIP] .env.example not found")
    print()


def init_database() -> None:
    """Initialize the SQLite database with schema."""
    print("Initializing database...")
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from database.connection import DatabaseManager
        from database.models import initialize_database

        db_path = str(PROJECT_ROOT / "data" / "counseling.db")
        db = DatabaseManager(db_path)
        initialize_database(db)
        db.close()
        print("  [OK] Database initialized")
    except Exception as e:
        print(f"  [WARN] Database init failed: {e}")
    print()


def main() -> None:
    """Run all initialization steps."""
    print("=" * 50)
    print("AI Counseling Assistant — Project Initialization")
    print("=" * 50)
    print()

    create_directories()
    setup_env()
    install_dependencies()
    download_spacy_model()
    init_database()

    print("=" * 50)
    print("Initialization complete!")
    print()
    print("Next steps:")
    print("  1. Review and customize .env if needed")
    print("  2. Ensure Ollama is running: ollama serve")
    print("  3. Pull a model: ollama pull llama3.2")
    print("  4. Run the app: streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
