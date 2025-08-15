from __future__ import annotations

from typing import Dict, List, Optional

import streamlit as st


def _format_value(value: float | int | str, fmt: Optional[str]) -> str:
    if isinstance(value, str):
        return value
    if fmt:
        try:
            return fmt.format(value)
        except Exception:
            return f"{value}"
    # default formatting with thousands separator
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def render_kpi_row(kpis: List[Dict]) -> None:
    """Render a horizontal row of KPI cards using Streamlit columns.

    Each KPI dict supports keys: 'label', 'value', optional 'format', optional 'help'.
    """
    num = max(1, len(kpis))
    cols = st.columns(num)
    for col, item in zip(cols, kpis):
        label = item.get("label", "KPI")
        value = item.get("value", "-")
        fmt = item.get("format")
        help_text = item.get("help")
        with col:
            st.metric(label=label, value=_format_value(value, fmt), help=help_text)


