import pandas as pd
import streamlit as st

from components.kpi_cards import render_kpi_row
from components.filters import render_filters
from components.menu import render_sidebar_menu
from components.layout import render_top_nav
from services.data_loader import load_sample_data
from viz.charts import build_time_series, build_bar_by_segment
from viz.plotly_3d import build_mini_3d_scene


st.set_page_config(page_title="Banking Dashboard", page_icon="💳", layout="wide")


def compute_kpis(dataframe: pd.DataFrame) -> list[dict]:
    total_customers = int(dataframe["customer_id"].nunique())
    total_balance = float(dataframe["balance"].sum())
    average_balance = float(dataframe["balance"].mean()) if not dataframe.empty else 0.0
    delinquency_rate = float(dataframe["delinquent"].mean() * 100.0) if "delinquent" in dataframe.columns else 0.0

    return [
        {"label": "Customers", "value": total_customers, "help": "Number of unique customers"},
        {"label": "Total balance (M€)", "value": total_balance / 1e6, "format": "{:,.2f}", "help": "Sum of all balances"},
        {"label": "Avg. balance (€)", "value": average_balance, "format": "{:,.0f}", "help": "Average balance per account"},
        {"label": "Delinquency rate (%)", "value": delinquency_rate, "format": "{:,.2f}", "help": "Share of accounts in default"},
    ]


def main() -> None:
    render_top_nav(active="home")
    render_sidebar_menu()
    st.title("Banking Dashboard")

    # Données et filtres
    df = load_sample_data()
    filters = render_filters(df)

    # Application des filtres simples
    mask = (df["date"] >= pd.to_datetime(filters["start_date"])) & (df["date"] <= pd.to_datetime(filters["end_date"]))
    if filters["segments"]:
        mask &= df["segment"].isin(filters["segments"])
    if filters["products"]:
        mask &= df["product"].isin(filters["products"])
    filtered = df.loc[mask].copy()

    # KPIs
    kpis = compute_kpis(filtered)
    render_kpi_row(kpis)

    # Graphiques 2D
    col_left, col_right = st.columns((2, 1))
    with col_left:
        st.subheader("Balance over time")
        st.plotly_chart(build_time_series(filtered), use_container_width=True)
    with col_right:
        st.subheader("Balance by segment")
        st.plotly_chart(build_bar_by_segment(filtered), use_container_width=True)

    # Mini scène 3D (MVP)
    st.subheader("Mini 3D scene – Indicator storytelling")
    st.caption("Hover to see values; click-drag to orbit the camera.")
    st.plotly_chart(build_mini_3d_scene(filtered), use_container_width=True)


if __name__ == "__main__":
    main()


