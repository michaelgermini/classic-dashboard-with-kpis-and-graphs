from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def build_mini_3d_scene(
    df: pd.DataFrame,
    metric: str = "sum_balance",
    colorscale: str = "Blues",
    bar_size: float = 0.4,
) -> go.Figure:
    """Simple 3D mini-scene: extruded bars by segment x product with metric selection.

    - X axis: segments
    - Y axis: products
    - Z axis: selected metric (sum/avg balance, accounts, delinquency rate)
    """
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No 3D data")
        return fig

    if "segment" not in df.columns or "product" not in df.columns:
        df = df.assign(segment="All", product="All")

    # Aggregate according to requested metric
    if metric == "avg_balance":
        agg = df.groupby(["segment", "product"], as_index=False)["balance"].mean().rename(columns={"balance": "value"})
        z_title = "Avg. balance (€)"
        colorbar_title = "Avg (€)"
    elif metric == "accounts":
        agg = df.groupby(["segment", "product"], as_index=False).size().rename(columns={"size": "value"})
        z_title = "Accounts"
        colorbar_title = "Accounts"
    elif metric == "delinquency_rate":
        if "delinquent" not in df.columns:
            df = df.assign(delinquent=0)
        agg = df.groupby(["segment", "product"], as_index=False)["delinquent"].mean()
        agg["value"] = agg["delinquent"].astype(float) * 100.0
        agg = agg.drop(columns=["delinquent"])  # keep segment, product, value
        z_title = "Delinquency rate (%)"
        colorbar_title = "%"
    else:  # sum_balance
        agg = df.groupby(["segment", "product"], as_index=False)["balance"].sum().rename(columns={"balance": "value"})
        z_title = "Balance (€)"
        colorbar_title = "€"
    segments = agg["segment"].unique().tolist()
    products = agg["product"].unique().tolist()

    x_pos = {s: i for i, s in enumerate(segments)}
    y_pos = {p: j for j, p in enumerate(products)}

    xs = np.array([x_pos[s] for s in agg["segment"]], dtype=float)
    ys = np.array([y_pos[p] for p in agg["product"]], dtype=float)
    heights = agg["value"].astype(float).to_numpy()

    # Create 3D bars using Mesh3d per bar (lightweight for small matrices)
    meshes = []
    for x, y, h, seg, prod in zip(xs, ys, heights, agg["segment"], agg["product"]):
        # Define the 8 vertices of the cuboid
        x0, x1 = x - bar_size, x + bar_size
        y0, y1 = y - bar_size, y + bar_size
        z0, z1 = 0.0, max(0.0, float(h))
        vertices = [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),  # bottom
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),  # top
        ]
        # Triangles indices for a box
        I, J, K = zip(
            # bottom
            (0, 1, 2), (0, 2, 3),
            # top
            (4, 5, 6), (4, 6, 7),
            # sides
            (0, 1, 5), (0, 5, 4),
            (1, 2, 6), (1, 6, 5),
            (2, 3, 7), (2, 7, 6),
            (3, 0, 4), (3, 4, 7),
        )
        hovertext = f"Segment: {seg}<br>Product: {prod}<br>Value: {h:,.2f}"
        # Intensity per vertex for colorscale (use top height for top vertices, 0 for bottom)
        intensities = [
            0.0, 0.0, 0.0, 0.0,  # bottom
            z1, z1, z1, z1       # top
        ]
        mesh = go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=list(I),
            j=list(J),
            k=list(K),
            opacity=0.95,
            intensity=intensities,
            colorscale=colorscale,
            showscale=False,
            flatshading=True,
            hovertext=hovertext,
            hoverinfo="text",
            lighting=dict(ambient=0.4, diffuse=0.7, specular=0.2),
        )
        meshes.append(mesh)

    fig = go.Figure(data=meshes)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Segment", tickmode="array", tickvals=list(range(len(segments))), ticktext=segments),
            yaxis=dict(title="Product", tickmode="array", tickvals=list(range(len(products))), ticktext=products),
            zaxis=dict(title=z_title),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.2)),
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        title="3D metric by segment and product",
        showlegend=False,
    )
    # Add a colorbar using a dummy scatter3d (for Mesh3d showscale per trace can be heavy)
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode="markers",
        marker=dict(size=0.0001, color=[0, 1], colorscale=colorscale, colorbar=dict(title=colorbar_title)),
        showlegend=False,
    ))
    return fig


