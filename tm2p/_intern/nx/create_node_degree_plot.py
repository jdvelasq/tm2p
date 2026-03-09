import plotly.express as px  # type: ignore

from tm2p.enum.column import DEGREE, NAME, NODE


def create_node_degree_plot(params, df):

    fig = px.line(
        df,
        x=NODE,
        y=DEGREE,
        hover_data=NAME,
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

    for _, row in df.iterrows():
        fig.add_annotation(
            x=row[NODE],
            y=row[DEGREE],
            text=row[NAME],
            showarrow=False,
            textangle=-90,
            yanchor="bottom",
            font={"size": params.textfont_size},
            yshift=params.yshift,
        )

    return fig
