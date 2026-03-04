import plotly.express as px  # type: ignore

CLUSTER_COLORS = (
    #
    # TABLEAU COLORS:
    # from matplotlib.colors.TABLEAU_COLORS
    [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    + px.colors.qualitative.Pastel1
    + px.colors.qualitative.Pastel2
    + px.colors.qualitative.Dark24
    + px.colors.qualitative.Light24
    + px.colors.qualitative.Set1
    + px.colors.qualitative.Set2
    + px.colors.qualitative.Set3
) * 10


def assign_node_colors_based_on_group_attribute(
    nx_graph,
):
    for node in nx_graph.nodes():
        group = nx_graph.nodes[node]["group"]
        nx_graph.nodes[node]["node_color"] = CLUSTER_COLORS[group]

    return nx_graph
