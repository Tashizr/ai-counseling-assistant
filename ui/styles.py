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

    /* Global - Dark theme */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #1a1a1a !important;
        color: #e0e0e0;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d !important;
    }
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] {
        background-color: #1a1a1a !important;
    }
    footer { visibility: hidden; }

    /* Main container */
    .block-container {
        padding-top: 2rem !important;
        max-width: 800px !important;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
        border: 1px solid #333;
        padding: 1.5rem 2rem;
        border-radius: 0.75rem;
        color: #e0e0e0;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: #f5f5f5 !important;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    .main-header p {
        color: #888;
        font-size: 0.85rem;
        margin: 0.5rem 0 0 0;
    }

    /* Disclaimer - Subtle dark */
    .disclaimer-box {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-left: 3px solid #b71c1c;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        color: #bbb;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* Crisis - Red accent */
    .crisis-box {
        background-color: #2d1111;
        border: 1px solid #5c1a1a;
        border-left: 3px solid #ef5350;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        color: #ef9a9a;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* Chat bubbles - ChatGPT style */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 1rem 0 !important;
        box-shadow: none !important;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1a1a1a !important;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #212121 !important;
    }
    div[data-testid="stChatMessageContent"] {
        color: #e0e0e0 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Chat input - ChatGPT style */
    .stChatInput {
        background-color: #2f2f2f !important;
        border: 1px solid #424242 !important;
        border-radius: 0.75rem !important;
    }
    .stChatInput:focus-within {
        border-color: #b71c1c !important;
        box-shadow: 0 0 0 1px #b71c1c !important;
    }
    .stChatInput textarea {
        color: #e0e0e0 !important;
        background-color: transparent !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d0d0d !important;
        border-right: 1px solid #222;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #888 !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.5rem 0.75rem;
        border-radius: 0.5rem;
        color: #999 !important;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.05);
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: rgba(183, 28, 28, 0.15);
        color: #ef5350 !important;
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .risk-low { background: #1b2e1b; color: #66bb6a; }
    .risk-moderate { background: #2e2a1b; color: #ffa726; }
    .risk-high { background: #2e1b1b; color: #ef5350; }
    .risk-critical { background: #b71c1c; color: white; }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #212121 !important;
        border: 1px solid #333;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    [data-testid="stMetric"] label {
        color: #888 !important;
    }
    [data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #e0e0e0 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #b71c1c !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #d32f2f !important;
        transform: translateY(-1px);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a;
        border-bottom: 1px solid #333;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888 !important;
        border-radius: 0;
        border-bottom: 2px solid transparent;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #e0e0e0 !important;
        border-bottom-color: #b71c1c;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #212121 !important;
        border: 1px solid #333;
        border-radius: 0.5rem;
        color: #ccc !important;
    }

    /* Text inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #2f2f2f !important;
        color: #e0e0e0 !important;
        border: 1px solid #424242 !important;
        border-radius: 0.5rem;
    }

    /* Success/Error/Warning boxes */
    .stAlert {
        background-color: #1e1e1e !important;
        border: 1px solid #333 !important;
        border-radius: 0.5rem;
    }

    /* Divider */
    hr {
        border-color: #333 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        color: #555;
    }
    .welcome-container h3 {
        color: #777;
        font-weight: 400;
    }
    .welcome-container p {
        color: #555;
        font-size: 0.9rem;
    }
    </style>
    """
