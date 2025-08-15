import pandas as pd
import streamlit as st
import plotly.express as px

from components.filters import render_filters
from components.menu import render_sidebar_menu
from components.layout import render_top_nav
from services.data_loader import load_sample_data


st.set_page_config(page_title="Risks", page_icon="⚠️", layout="wide")


def build_delinquency_timeseries(df: pd.DataFrame):
    if df.empty or "delinquent" not in df.columns:
        return px.line(title="Aucune donnée")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.floor("D")
    daily = df.groupby("date", as_index=False)["delinquent"].mean()
    daily["delinquency_rate"] = daily["delinquent"] * 100.0
    fig = px.line(daily, x="date", y="delinquency_rate", markers=True, title="Taux de défaut quotidien (%)")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def build_delinquency_by_segment(df: pd.DataFrame):
    if df.empty or not {"segment", "delinquent"}.issubset(df.columns):
        return px.bar(title="Aucune donnée")
    agg = df.groupby("segment", as_index=False)["delinquent"].mean()
    agg["rate"] = agg["delinquent"] * 100.0
    fig = px.bar(agg, x="segment", y="rate", title="Taux de défaut par segment (%)")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def build_distribution_balance(df: pd.DataFrame):
    if df.empty or "balance" not in df.columns:
        return px.histogram(title="Aucune donnée")
    fig = px.histogram(df, x="balance", nbins=50, title="Distribution des encours")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def main() -> None:
    render_top_nav(active="risks")
    render_sidebar_menu()
    st.title("Risks")

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
        st.subheader("Taux de défaut quotidien")
        st.plotly_chart(build_delinquency_timeseries(filtered), use_container_width=True)
    with col2:
        st.subheader("Taux de défaut par segment")
        st.plotly_chart(build_delinquency_by_segment(filtered), use_container_width=True)

    st.subheader("Distribution des encours")
    st.plotly_chart(build_distribution_balance(filtered), use_container_width=True)


if __name__ == "__main__":
    main()


