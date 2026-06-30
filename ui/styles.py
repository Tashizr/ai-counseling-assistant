"""
Custom CSS styling for the Streamlit UI.
"""


def get_custom_css() -> str:
    """Return custom CSS for the counseling assistant UI."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Base */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #171717;
    }
    header[data-testid="stHeader"] { background: #171717; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }

    /* Layout */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 760px !important;
    }

    /* Header */
    .main-header {
        background: #1e1e1e;
        border: 1px solid #2a2a2a;
        padding: 1rem 1.25rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        color: #e8e8e8 !important;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0;
        line-height: 1.3;
    }
    .main-header p {
        color: #666;
        font-size: 0.78rem;
        margin: 0.25rem 0 0 0;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: #1c1c1c;
        border: 1px solid #2a2a2a;
        border-left: 2px solid #555;
        border-radius: 0.35rem;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.75rem;
        color: #888;
        font-size: 0.75rem;
        line-height: 1.45;
    }

    /* Crisis */
    .crisis-box {
        background: #1f1414;
        border: 1px solid #3d1c1c;
        border-left: 2px solid #b71c1c;
        border-radius: 0.35rem;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.75rem;
        color: #cc8888;
        font-size: 0.75rem;
        line-height: 1.45;
    }

    /* Chat messages */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0.75rem 0 !important;
        box-shadow: none !important;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) { background: #171717; }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) { background: #1e1e1e; }
    div[data-testid="stChatMessageContent"] {
        color: #d4d4d4 !important;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    /* Chat input */
    .stChatInput {
        background: #2a2a2a !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 0.5rem !important;
    }
    .stChatInput:focus-within {
        border-color: #555 !important;
    }
    .stChatInput textarea { color: #d4d4d4 !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111 !important;
        border-right: 1px solid #222;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.4rem 0.6rem;
        border-radius: 0.35rem;
        color: #777 !important;
        font-size: 0.82rem;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.04);
        color: #ccc !important;
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    .risk-low { background: #162016; color: #5a9a5a; }
    .risk-moderate { background: #201c10; color: #b8944a; }
    .risk-high { background: #201414; color: #c45050; }
    .risk-critical { background: #5c1a1a; color: #ff8a8a; }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #1e1e1e;
        border: 1px solid #2a2a2a;
        padding: 0.6rem 0.75rem;
        border-radius: 0.35rem;
    }
    [data-testid="stMetric"] label { color: #666 !important; font-size: 0.7rem !important; }
    [data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #d4d4d4 !important;
        font-size: 1rem !important;
    }

    /* Buttons */
    .stButton > button {
        background: #b71c1c !important;
        color: #fff !important;
        border: none !important;
        border-radius: 0.35rem;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.35rem 1rem;
    }
    .stButton > button:hover { background: #c62828 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a1a;
        border-bottom: 1px solid #2a2a2a;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #666 !important;
        border-radius: 0;
        border-bottom: 2px solid transparent;
        font-size: 0.82rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #d4d4d4 !important;
        border-bottom-color: #b71c1c;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #1e1e1e !important;
        border: 1px solid #2a2a2a;
        border-radius: 0.35rem;
        color: #aaa !important;
        font-size: 0.82rem;
    }

    /* Text/Number inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #252525 !important;
        color: #d4d4d4 !important;
        border: 1px solid #333 !important;
        border-radius: 0.35rem;
    }

    /* Alerts */
    .stAlert {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 0.35rem;
        font-size: 0.82rem;
    }

    /* Dividers */
    hr { border-color: #252525 !important; margin: 0.75rem 0 !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

    /* Welcome */
    .welcome-container {
        text-align: center;
        padding: 3rem 1rem;
        color: #444;
    }
    .welcome-container h3 {
        color: #555;
        font-weight: 400;
        font-size: 1rem;
    }
    .welcome-container p {
        color: #444;
        font-size: 0.8rem;
    }

    /* File uploader */
    .stFileUploader { border: 1px solid #333; border-radius: 0.35rem; padding: 0.5rem; }

    /* Selectbox */
    .stSelectbox > div > div { background: #252525 !important; color: #d4d4d4 !important; }
    </style>
    """
