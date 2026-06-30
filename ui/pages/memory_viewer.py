"""
Memory viewer page for inspecting stored memories.
"""

import streamlit as st


def render_memory_viewer_page() -> None:
    """Render the memory viewer page."""
    st.title("Memory Viewer")

    st.markdown(
        "View and manage what the assistant remembers about your conversations."
    )

    if "long_term_memory" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    ltm = st.session_state.long_term_memory
    user_id = st.session_state.get("user_id", "default_user")

    tab1, tab2 = st.tabs(["Long-Term Memory", "Short-Term Context"])

    with tab1:
        memories = ltm.retrieve_memories(user_id, limit=20)
        if not memories:
            st.info("No long-term memories stored yet.")
        else:
            for mem in memories:
                with st.expander(
                    f"[{mem['category']}] Importance: {mem['importance']}/5"
                ):
                    st.write(mem["content"])
                    st.caption(f"Created: {mem['created_at']}")
                    st.caption(f"Accessed: {mem['accessed_at']}")
                    if mem.get("expires_at"):
                        st.caption(f"Expires: {mem['expires_at']}")

    with tab2:
        if "engine" in st.session_state:
            context = st.session_state.engine.get_conversation_context()
            if context:
                st.text_area(
                    "Current Conversation Context",
                    value=context,
                    height=300,
                    disabled=True,
                )
            else:
                st.info("No current conversation context.")
        else:
            st.info("Engine not initialized.")
