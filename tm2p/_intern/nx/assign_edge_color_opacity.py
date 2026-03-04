import colorsys

import numpy as np


def assign_edge_color_opacity(
    params,
    nx_graph,
):

    # Convert hex color to RGB
    hex_color = params.edge_colors[0]
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # Extract edge weights
    widths = np.array([nx_graph.edges[edge]["width"] for edge in nx_graph.edges()])

    # Compute opacity based on edge width
    if widths.max() == widths.min():
        opacities = np.full_like(widths, 1.0)
    else:
        opacities = (widths - widths.min()) / (widths.max() - widths.min())
    opacities = (
        opacities * (params.edge_opacity_range[1] - params.edge_opacity_range[0])
        + params.edge_opacity_range[0]
    )

    rgb_colors = [
        colorsys.hls_to_rgb(h, l * (1.0 - opacity), s) for opacity in opacities
    ]

    rgb_colors = [
        f"rgb({r}, {g}, {b}, {round(opacity, 4)})"
        for (r, g, b), opacity in zip(rgb_colors, opacities)
    ]

    for edge, color in zip(nx_graph.edges(), rgb_colors):
        nx_graph.edges[edge]["color"] = color

    return nx_graph
