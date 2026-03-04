"""Node degree plot"""

from dataclasses import dataclass
from typing import Optional

import networkx as nx  # type: ignore
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore


def create_node_degree_plot(params, data_frame):

    fig = px.line(
        data_frame,
        x="Node",
        y="Degree",
        hover_data="Name",
        markers=True,
    )
    fig.update_traces(
        marker={
            "size": params.marker_size,
            "line": {"color": params.line_color, "width": 0},
        },
        marker_color=params.line_color,
        line={
            "color": params.line_color,
            "width": params.line_width,
        },
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_yaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
        title="Degree",
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="lightgray",
        griddash="dot",
        title="Node",
    )

    for _, row in data_frame.iterrows():
        fig.add_annotation(
            x=row["Node"],
            y=row["Degree"],
            text=row["Name"],
            showarrow=False,
            textangle=-90,
            yanchor="bottom",
            font={"size": params.textfont_size},
            yshift=params.yshift,
        )

    return fig
