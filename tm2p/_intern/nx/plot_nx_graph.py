import plotly.graph_objects as go  # type: ignore


def internal__plot_nx_graph(
    params,
    nx_graph,
):

    xaxes_range = params.xaxes_range
    yaxes_range = params.yaxes_range
    axes_visible = params.axes_visible
    draw_arrows = params.draw_arrows

    node_trace = __create_node_trace(nx_graph)
    edge_traces = __create_edge_traces(nx_graph)

    fig = __create_network_fig(
        edge_traces,
        node_trace,
        xaxes_range,
        yaxes_range,
        axes_visible,
    )

    fig = __add_node_labels_to_fig(fig, nx_graph)

    fig = __draw_arrows(fig, nx_graph, draw_arrows)

    return fig


def __draw_arrows(fig, nx_graph, draw_arrows):
    if draw_arrows is False:
        return fig

    for edge in nx_graph.edges():
        node_citing_article = edge[0]
        node_cited_article = edge[1]

        citing_x = nx_graph.nodes[node_citing_article]["x"]
        citing_y = nx_graph.nodes[node_citing_article]["y"]
        cited_x = nx_graph.nodes[node_cited_article]["x"]
        cited_y = nx_graph.nodes[node_cited_article]["y"]

        head_x = (citing_x + cited_x) / 2
        head_y = (citing_y + cited_y) / 2

        ax = head_x - (cited_x - citing_x) / 2 * 0.5
        ay = head_y - (cited_y - citing_y) / 2 * 0.5

        fig.add_annotation(
            axref="x",
            ayref="y",
            x=head_x,
            y=head_y,
            ax=ax,
            ay=ay,
            showarrow=True,
            arrowhead=4,
            arrowsize=2,
            arrowcolor="#7793a5",
            arrowwidth=0.7,
        )

    return fig


def __create_node_trace(nx_graph):
    """Creates a node trace for a networkx graph."""

    node_x = [data["x"] for _, data in nx_graph.nodes(data=True)]
    node_y = [data["y"] for _, data in nx_graph.nodes(data=True)]
    node_color = [data["node_color"] for _, data in nx_graph.nodes(data=True)]
    node_size = [data["node_size"] for _, data in nx_graph.nodes(data=True)]
    node_text = [data["text"] for _, data in nx_graph.nodes(data=True)]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        text=node_text,
        hoverinfo="text",
        marker={
            "color": node_color,
            "size": node_size,
            "line": {"width": 1.5, "color": "white"},
            "opacity": 1.0,
        },
    )

    return node_trace


def __create_edge_traces(graph):
    """Creates edge traces for a networkx graph."""

    edge_traces = []

    data = []

    for edge in graph.edges():
        #
        pos_x0 = graph.nodes[edge[0]]["x"]
        pos_y0 = graph.nodes[edge[0]]["y"]
        #
        pos_x1 = graph.nodes[edge[1]]["x"]
        pos_y1 = graph.nodes[edge[1]]["y"]
        #
        color = graph.edges[edge]["color"]
        dash = graph.edges[edge]["dash"]
        width = graph.edges[edge]["width"]

        edge_trace = go.Scatter(
            x=(pos_x0, pos_x1),
            y=(pos_y0, pos_y1),
            line={
                "color": color,
                "dash": dash,
                "width": width,
            },
            hoverinfo="none",
            mode="lines",
        )

        # edge_traces.append(edge_trace)
        data.append((edge_trace, width))

    #
    # Ascending order
    data = sorted(data, key=lambda x: x[1])
    edge_traces = [x[0] for x in data]

    return edge_traces


def __create_network_fig(
    edge_traces,
    node_trace,
    xaxes_range,
    yaxes_range,
    axes_visible,
):
    """Creates a network graph from traces using plotly express."""

    layout = go.Layout(
        title="",
        font={"size": 16},
        showlegend=False,
        hovermode="closest",
        margin={"b": 0, "l": 0, "r": 0, "t": 0},
        annotations=[
            {
                "text": "",
                "showarrow": False,
                "xref": "paper",
                "yref": "paper",
                "x": 0.005,
                "y": -0.002,
                "align": "left",
                "font": {"size": 10},
            }
        ],
    )

    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=layout,
    )

    if axes_visible is False:
        fig.update_layout(
            xaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
            },
        )

    if xaxes_range is not None:
        fig.update_xaxes(range=xaxes_range)

    if yaxes_range is not None:
        fig.update_yaxes(range=yaxes_range)

    fig.update_layout(
        hoverlabel={
            "bgcolor": "white",
            "font_family": "monospace",
        },
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return fig


def __add_node_labels_to_fig(fig, nx_graph):

    node_x = [data["x"] for _, data in sorted(nx_graph.nodes(data=True))]
    node_y = [data["y"] for _, data in sorted(nx_graph.nodes(data=True))]
    node_labels = [data["text"] for _, data in sorted(nx_graph.nodes(data=True))]
    node_labeled = [data["labeled"] for _, data in sorted(nx_graph.nodes(data=True))]

    textfont_sizes = [
        data["textfont_size"] for _, data in sorted(nx_graph.nodes(data=True))
    ]
    textfont_opacities = [
        data["textfont_opacity"] for _, data in sorted(nx_graph.nodes(data=True))
    ]

    textpositions = [
        data["textposition"] for _, data in sorted(nx_graph.nodes(data=True))
    ]

    #
    node_x.reverse()
    node_y.reverse()
    node_labels.reverse()
    node_labeled.reverse()
    textfont_sizes.reverse()
    textpositions.reverse()
    textfont_opacities.reverse()

    #

    for pos_x, pos_y, name, textfont_size, textpos, textcolor, labeled in zip(
        node_x,
        node_y,
        node_labels,
        textfont_sizes,
        textpositions,
        textfont_opacities,
        node_labeled,
    ):
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
            xshift = 0
            yshift = 0

        if labeled is True:
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
                opacity=textcolor,
            )

    return fig
