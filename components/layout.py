from __future__ import annotations

import streamlit as st


def render_top_nav(active: str = "home") -> None:
    """Render a simple sticky top navigation bar with buttons to switch pages.

    active: one of {"home", "overview", "portfolio", "risks", "story3d"}
    """
    st.markdown(
        """
        <style>
        .top-nav {
            position: sticky; top: 0; z-index: 999;
            background: var(--background-color, #FFFFFF);
            padding: 0.5rem 0.75rem; margin-bottom: 0.5rem;
            border-bottom: 1px solid rgba(0,0,0,0.06);
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }
        .top-nav-title { font-weight: 700; font-size: 1.05rem; }
        .top-nav-spacer { height: 2px; }
        </style>
        <div class="top-nav"></div>
        <div class="top-nav-spacer"></div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 3])
    with left:
        st.markdown("**💳 Banking Dashboard**")
    with right:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("🏠 Home", type="secondary", help="Home") and active != "home":
                st.switch_page("app.py")
        with c2:
            if st.button("📊 Overview", type="secondary", help="Overview") and active != "overview":
                st.switch_page("pages/1_Overview.py")
        with c3:
            if st.button("📁 Portfolio", type="secondary", help="Portfolio") and active != "portfolio":
                st.switch_page("pages/2_Portfolio.py")
        with c4:
            if st.button("⚠️ Risks", type="secondary", help="Risks") and active != "risks":
                st.switch_page("pages/3_Risks.py")
        with c5:
            if st.button("🧊 3D", type="secondary", help="3D Storytelling") and active != "story3d":
                st.switch_page("pages/4_3D_Storytelling.py")


