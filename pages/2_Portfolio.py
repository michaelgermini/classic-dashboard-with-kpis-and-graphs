import pandas as pd
import streamlit as st

from components.filters import render_filters
from components.menu import render_sidebar_menu
from components.layout import render_top_nav
from services.data_loader import load_sample_data
from viz.charts import build_bar_by_segment
import plotly.express as px


st.set_page_config(page_title="Portfolio", page_icon="📁", layout="wide")


def build_bar_by_product(df: pd.DataFrame):
    if df.empty or "product" not in df.columns:
        return px.bar(title="No data")
    agg = df.groupby("product", as_index=False)["balance"].sum().sort_values("balance", ascending=False)
    fig = px.bar(agg, x="product", y="balance", title="Balance by product")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def build_heatmap_segment_product(df: pd.DataFrame):
    if df.empty or not {"segment", "product"}.issubset(df.columns):
        return px.imshow([[0]], labels=dict(x="Product", y="Segment", color="Balance"), title="No data")
    pivot = df.pivot_table(index="segment", columns="product", values="balance", aggfunc="sum", fill_value=0.0)
    fig = px.imshow(
        pivot,
        labels=dict(x="Product", y="Segment", color="Balance"),
        title="Heatmap balance: segment x product",
        aspect="auto",
        color_continuous_scale="Blues",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def main() -> None:
    render_top_nav(active="portfolio")
    render_sidebar_menu()
    st.title("Portfolio")

    df = load_sample_data()
    filters = render_filters(df)

    mask = (df["date"] >= pd.to_datetime(filters["start_date"])) & (df["date"] <= pd.to_datetime(filters["end_date"]))
    if filters["segments"]:
        mask &= df["segment"].isin(filters["segments"])
    if filters["products"]:
        mask &= df["product"].isin(filters["products"])
    filtered = df.loc[mask].copy()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Encours par produit")
        st.plotly_chart(build_bar_by_product(filtered), use_container_width=True)
    with col2:
        st.subheader("Encours par segment")
        st.plotly_chart(build_bar_by_segment(filtered), use_container_width=True)

    st.subheader("Composition segment x produit")
    st.plotly_chart(build_heatmap_segment_product(filtered), use_container_width=True)


if __name__ == "__main__":
    main()


