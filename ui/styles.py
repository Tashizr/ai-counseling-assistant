"""
Custom CSS styling for the Streamlit UI.
"""


def get_custom_css() -> str:
    """Return custom CSS for the counseling assistant UI.

    Returns:
        CSS string for Streamlit injection.
    """
    return """
    <style>
    .stApp {
        max-width: 900px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .chat-message.assistant {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .disclaimer-box {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .crisis-box {
        background-color: #ffebee;
        border: 2px solid #f44336;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .mood-indicator {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    .risk-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .risk-low { background-color: #c8e6c9; color: #2e7d32; }
    .risk-moderate { background-color: #fff9c4; color: #f57f17; }
    .risk-high { background-color: #ffcdd2; color: #c62828; }
    .risk-critical { background-color: #f44336; color: white; }
    </style>
    """
