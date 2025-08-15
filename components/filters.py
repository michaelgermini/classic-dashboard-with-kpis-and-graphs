from __future__ import annotations

import datetime as dt
from typing import Dict, List

import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> Dict:
    min_date = pd.to_datetime(df["date"]).min() if "date" in df.columns else pd.Timestamp.today() - pd.Timedelta(days=365)
    max_date = pd.to_datetime(df["date"]).max() if "date" in df.columns else pd.Timestamp.today()

    with st.sidebar:
        st.header("Filters")
        start_date = st.date_input("Start date", value=min_date.date(), min_value=min_date.date(), max_value=max_date.date())
        end_date = st.date_input("End date", value=max_date.date(), min_value=min_date.date(), max_value=max_date.date())

        segments: List[str] = []
        products: List[str] = []
        if "segment" in df.columns:
            segs = sorted([s for s in df["segment"].dropna().unique().tolist()])
            segments = st.multiselect("Segments", segs, default=segs)
        if "product" in df.columns:
            prods = sorted([p for p in df["product"].dropna().unique().tolist()])
            products = st.multiselect("Products", prods, default=prods)

    return {
        "start_date": pd.Timestamp(start_date),
        "end_date": pd.Timestamp(end_date),
        "segments": segments,
        "products": products,
    }


