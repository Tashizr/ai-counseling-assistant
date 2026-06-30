"""
Memory viewer page for inspecting stored memories.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_memory_viewer_page() -> None:
    """Render the memory viewer page."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>🧠 Memory</h1>
            <p>What I remember about our conversations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "long_term_memory" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    ltm = st.session_state.long_term_memory
    user_id = st.session_state.get("user_id", "default_user")

    tab1, tab2 = st.tabs(["Long-Term", "Current Session"])

    with tab1:
        memories = ltm.retrieve_memories(user_id, limit=20)
        if not memories:
            st.info("No long-term memories yet.")
        else:
            for mem in memories:
                with st.expander(f"[{mem['category']}] Priority {mem['importance']}/5"):
                    st.write(mem["content"])
                    st.caption(f"Created: {mem['created_at']}")

    with tab2:
        if "engine" in st.session_state:
            context = st.session_state.engine.get_conversation_context()
            if context:
                st.text_area("Context", value=context, height=300, disabled=True)
            else:
                st.info("No current context.")
