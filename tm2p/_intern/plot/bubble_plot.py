import pandas as pd
import plotly.express as px  # type: ignore

from tm2p._intern import Params


def bubble_plot(
    params: Params,
    x_name: str,
    y_name: str,
    size_col: str,
    dataframe: pd.DataFrame,
):

    fig = px.scatter(
        dataframe,
        x=x_name,
        y=y_name,
        size=size_col,
        hover_data=dataframe.columns.to_list(),
        title=params.title_text,
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        yaxis_title=params.yaxes_title_text,
        xaxis_title=params.xaxes_title_text,
        margin={"l": 1, "r": 1, "t": 1, "b": 1},
    )
    fig.update_traces(
        marker={"line": {"color": "black", "width": 2}},
        marker_color="darkslategray",
        mode="markers",
    )
    fig.update_xaxes(
        side="top",
        linecolor="white",
        linewidth=1,
        gridcolor="gray",
        griddash="dot",
        tickangle=270,
        dtick=1.0,
    )
    fig.update_yaxes(
        linecolor="white",
        linewidth=1,
        gridcolor="gray",
        griddash="dot",
        autorange="reversed",
    )

    return fig
