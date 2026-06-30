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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        color: white !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: none;
        border-left: 4px solid #4caf50;
        border-radius: 0.75rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        color: #2e7d32;
        font-size: 0.88rem;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
    }

    /* Crisis */
    .crisis-box {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        border: none;
        border-left: 4px solid #e91e63;
        border-radius: 0.75rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        color: #880e4f;
        font-size: 0.88rem;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(233, 30, 99, 0.1);
    }

    /* Chat bubbles */
    .stChatMessage {
        border-radius: 1rem;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        border: none;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    .risk-low {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .risk-moderate {
        background: #fff3e0;
        color: #e65100;
    }
    .risk-high {
        background: #fce4ec;
        color: #c62828;
    }
    .risk-critical {
        background: #c62828;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #ccc;
    }
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.5rem 0.75rem;
        border-radius: 0.5rem;
        transition: all 0.2s;
        color: #e0e0e0;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.1);
    }

    /* Input area */
    .stChatInput {
        border-radius: 1rem;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stChatInput:focus-within {
        border-color: #667eea;
        box-shadow: 0 2px 12px rgba(102, 126, 234, 0.2);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 500;
        border-radius: 0.5rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.5rem 1.5rem;
    }
    </style>
    """
