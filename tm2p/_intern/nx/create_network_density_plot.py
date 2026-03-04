import numpy as np
import pandas as pd  # type: ignore
import plotly.graph_objects as go
from sklearn.neighbors import KernelDensity


def create_network_density_plot(
    params,
    nx_graph,
):
    bandwidth = params.kernel_bandwidth
    colorscale = params.colormap
    opacity = params.contour_opacity

    #
    # Network node positions
    node_x = [data["x"] for _, data in nx_graph.nodes(data=True)]
    node_y = [data["y"] for _, data in nx_graph.nodes(data=True)]

    nodes = pd.DataFrame({"x": node_x, "y": node_y})

    #
    # Compute density
    kde = KernelDensity(bandwidth=bandwidth, kernel="gaussian").fit(nodes)

    #
    # Create a grid for plotting
    x_range = nodes["x"].max() - nodes["x"].min()
    x_max = nodes["x"].max() + 0.05 * x_range
    x_min = nodes["x"].min() - 0.05 * x_range

    y_range = nodes["y"].max() - nodes["y"].min()
    y_max = nodes["y"].max() + 0.05 * y_range
    y_min = nodes["y"].min() - 0.05 * y_range

    x_plot = np.linspace(x_min, x_max, 100)
    y_plot = np.linspace(y_min, y_max, 100)
    x_mtx_plot, y_mtx_plot = np.meshgrid(x_plot, y_plot)
    xy_plot = np.vstack([x_mtx_plot.ravel(), y_mtx_plot.ravel()]).T
    z_mtx = np.exp(kde.score_samples(xy_plot))
    z_mtx = z_mtx.reshape(x_mtx_plot.shape)

    fig = go.Figure(
        data=go.Contour(
            z=z_mtx,
            x=x_plot,
            y=y_plot,
            opacity=opacity,
            showscale=False,
            colorscale=colorscale,
        )
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin={"l": 1, "r": 1, "t": 1, "b": 1},
    )
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

    fig.update_xaxes(range=[x_min, x_max])
    fig.update_yaxes(range=[y_min, y_max])

    #
    # Labels:
    node_labels = [data["text"] for _, data in nx_graph.nodes(data=True)]
    textfont_sizes = [data["textfont_size"] for _, data in nx_graph.nodes(data=True)]

    for pos_x, pos_y, name, textfont_size in zip(
        node_x, node_y, node_labels, textfont_sizes
    ):
        fig.add_annotation(
            x=pos_x,
            y=pos_y,
            text=name,
            showarrow=False,
            font={"size": textfont_size},
            # bordercolor="grey",
            # bgcolor="white",
            # xanchor=xanchor,
            # yanchor=yanchor,
            # xshift=xshift,
            # yshift=yshift,
        )

    return fig
