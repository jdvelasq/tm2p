import plotly.graph_objects as go

from tm2p._intern.utils.utils_compute_textposition_from_x_and_y import (
    _utils_compute_textposition_from_x_and_y,
)


def manifold_2d_map(
    node_x,
    node_y,
    node_text,
    node_color=None,
    node_size=30,
    title_x=None,
    title_y=None,
    textfont_size=10,
    textfont_color="#465c6b",
    xaxes_range=None,
    yaxes_range=None,
    remove_occ_gc=True,
):
    """Makes a scatter plot."""

    if remove_occ_gc:
        node_text = [" ".join(text.split(" ")[:-1]) for text in node_text]

    textpositions = _utils_compute_textposition_from_x_and_y(node_x, node_y)

    fig = go.Figure(
        layout=go.Layout(
            xaxis={"mirror": "allticks"},
            yaxis={"mirror": "allticks"},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            textposition=textpositions,
            text=node_text,
        )
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=1, r=1, t=1, b=1),
    )

    fig.update_traces(
        marker=dict(
            line=dict(color="#b8c6d0", width=1),
            opacity=0.8,
        ),
        marker_color=node_color,
        marker_size=node_size,
        textfont_size=textfont_size,
        textfont_color=textfont_color,
    )

    fig.update_xaxes(
        linecolor="white",
        linewidth=1,
        gridcolor="lightgray",
        griddash="dot",
        ticks="outside",
        tickwidth=2,
        ticklen=10,
        minor=dict(ticklen=5),
        title=title_x if title_x is not None else "",
    )

    fig.update_yaxes(
        linecolor="white",
        linewidth=1,
        gridcolor="lightgray",
        griddash="dot",
        ticks="outside",
        tickwidth=2,
        ticklen=10,
        minor=dict(ticklen=5),
        title=title_y if title_y is not None else "",
    )

    for pos_x, pos_y, name, textpos in zip(node_x, node_y, node_text, textpositions):
        if textpos == "top right":
            xanchor = "left"
            yanchor = "bottom"
            xshift = 4
            yshift = 4
        elif textpos == "top left":
            xanchor = "right"
            yanchor = "bottom"
            xshift = -4
            yshift = 4
        elif textpos == "bottom right":
            xanchor = "left"
            yanchor = "top"
            xshift = 4
            yshift = -4
        elif textpos == "bottom left":
            xanchor = "right"
            yanchor = "top"
            xshift = -4
            yshift = -4
        else:
            xanchor = "center"
            yanchor = "center"

        fig.add_annotation(
            x=pos_x,
            y=pos_y,
            text=name,
            showarrow=False,
            font={"size": textfont_size},
            bordercolor="grey",
            bgcolor="white",
            xanchor=xanchor,
            yanchor=yanchor,
            xshift=xshift,
            yshift=yshift,
        )

    if xaxes_range is not None:
        fig.update_xaxes(range=xaxes_range)

    if yaxes_range is not None:
        fig.update_yaxes(range=yaxes_range)

    return fig
