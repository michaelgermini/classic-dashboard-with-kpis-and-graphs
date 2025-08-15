from __future__ import annotations

import pandas as pd
import plotly.express as px


def build_time_series(df: pd.DataFrame):
    if df.empty:
        return px.line(title="No data")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.floor("D")
    daily = df.groupby("date", as_index=False)["balance"].sum()
    fig = px.line(daily, x="date", y="balance", markers=True, title="Daily aggregated balance")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def build_bar_by_segment(df: pd.DataFrame):
    if df.empty or "segment" not in df.columns:
        return px.bar(title="No data")
    agg = df.groupby("segment", as_index=False)["balance"].sum().sort_values("balance", ascending=False)
    fig = px.bar(agg, x="segment", y="balance", title="Balance by segment")
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


