from __future__ import annotations

import streamlit as st


def render_sidebar_menu() -> None:
    with st.sidebar:
        st.markdown("---")
        st.caption("Navigation")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Overview.py", label="Overview", icon="📊")
        st.page_link("pages/2_Portfolio.py", label="Portfolio", icon="📁")
        st.page_link("pages/3_Risks.py", label="Risks", icon="⚠️")
        st.page_link("pages/4_3D_Storytelling.py", label="3D Storytelling", icon="🧊")
        st.markdown("---")


