from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_sample_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Load sample banking data. If no file exists, generate a synthetic dataset.

    Columns: date, customer_id, segment, product, balance, delinquent
    """
    if csv_path is None:
        csv_path = os.path.join("data", "sample", "transactions.csv")
    path = Path(csv_path)
    if path.exists():
        df = pd.read_csv(path)
        df["date"] = pd.to_datetime(df["date"])
        # Normalize any previously generated French product names to English
        if "product" in df.columns:
            fr_to_en_products = {
                "Courant": "Current",
                "Épargne": "Savings",
                "Epargne": "Savings",
                "Crédit": "Loan",
                "Credit": "Loan",
                "Invest": "Invest",
                "Tous": "All",
            }
            df["product"] = df["product"].replace(fr_to_en_products)
        return df

    # Generate synthetic dataset
    rng = np.random.default_rng(42)
    num_days = 180
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=num_days)
    segments = ["Retail", "Affluent", "SME", "Corporate"]
    products = ["Current", "Savings", "Loan", "Invest"]
    num_customers = 1200

    customer_ids = np.arange(100000, 100000 + num_customers)
    customer_segments = rng.choice(segments, size=num_customers, p=[0.5, 0.2, 0.2, 0.1])

    rows = []
    for day in dates:
        # random subset of customers active daily
        active = rng.choice(customer_ids, size=rng.integers(num_customers // 3, num_customers // 2), replace=False)
        for cid in active:
            seg = customer_segments[cid - 100000]
            prod = rng.choice(products, p=[0.45, 0.35, 0.15, 0.05])
            base = {
                "Current": 1500,
                "Savings": 8000,
                "Loan": -12000,
                "Invest": 20000,
            }[prod]
            noise = rng.normal(0, 2000)
            balance = max(-20000, base + noise)
            delinquent = int(balance < -5000 and rng.random() < 0.15)
            rows.append([day, cid, seg, prod, float(balance), delinquent])

    df = pd.DataFrame(rows, columns=["date", "customer_id", "segment", "product", "balance", "delinquent"])
    # Save for reuse
    out_dir = Path("data", "sample")
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "transactions.csv", index=False)
    return df


