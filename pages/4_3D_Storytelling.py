import pandas as pd
import streamlit as st

from components.filters import render_filters
from components.menu import render_sidebar_menu
from components.layout import render_top_nav
from services.data_loader import load_sample_data
from viz.plotly_3d import build_mini_3d_scene


st.set_page_config(page_title="3D Storytelling", page_icon="🧊", layout="wide")


def main() -> None:
    render_top_nav(active="story3d")
    render_sidebar_menu()
    st.title("3D Storytelling")
    st.caption("Explore KPIs in an interactive 3D scene. Hover to inspect, click-drag to orbit.")

    df = load_sample_data()
    filters = render_filters(df)

    mask = (df["date"] >= pd.to_datetime(filters["start_date"])) & (df["date"] <= pd.to_datetime(filters["end_date"]))
    if filters["segments"]:
        mask &= df["segment"].isin(filters["segments"])
    if filters["products"]:
        mask &= df["product"].isin(filters["products"])
    filtered = df.loc[mask].copy()

    with st.sidebar:
        st.subheader("3D Options")
        metric = st.selectbox(
            "Metric",
            options=[
                ("Sum of balances", "sum_balance"),
                ("Average balance", "avg_balance"),
                ("Number of accounts", "accounts"),
                ("Delinquency rate (%)", "delinquency_rate"),
            ],
            format_func=lambda x: x[0],
        )[1]
        colorscale = st.selectbox("Colorscale", ["Blues", "Viridis", "Cividis", "Plasma", "Inferno", "Magma"]) 
        bar_size = st.slider("Bar thickness", min_value=0.2, max_value=0.8, value=0.4, step=0.05)

    st.plotly_chart(
        build_mini_3d_scene(filtered, metric=metric, colorscale=colorscale, bar_size=bar_size),
        use_container_width=True,
    )


if __name__ == "__main__":
    main()


