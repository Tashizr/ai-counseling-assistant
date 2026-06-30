"""
Memory viewer page.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_memory_viewer_page() -> None:
    """Render memory viewer."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        '<div class="main-header"><h1>🧠 Memory</h1>'
        '<p>What I remember about you.</p></div>',
        unsafe_allow_html=True,
    )

    if "long_term_memory" not in st.session_state:
        st.warning("Initialize the application first.")
        return

    ltm = st.session_state.long_term_memory
    uid = st.session_state.get("user_id", "default")

    tab1, tab2 = st.tabs(["Long-Term", "Current"])

    with tab1:
        mems = ltm.retrieve_memories(uid, limit=20)
        if not mems:
            st.info("No memories yet.")
        for m in mems:
            with st.expander(f"{m['category']} — priority {m['importance']}/5"):
                st.write(m["content"])

    with tab2:
        if "engine" in st.session_state:
            ctx = st.session_state.engine.get_conversation_context()
            if ctx:
                st.text_area("Context", ctx, height=250, disabled=True)
            else:
                st.info("No current context.")
