"""
Treemap
===============================================================================


# >>> from tm2p.nx_visualize_treemap import nx_visualize_treemap
# >>> itemslist = tm2pplus.list_items(
# ...    field='author_keywords',
# ...    top_n=20,
# ...    root_dir=root_dir,
# ... )
# >>> plot = treemap(itemslist, title="Most Frequent Author Keywords")
# >>> plot.plot_.write_html(file_name)

# .. raw:: html

#     <iframe src="../_static/treemap.html" height="600px" width="100%" frameBorder="0"></iframe>

"""

import plotly.graph_objs as go  # type: ignore

from tm2p._intern.nx.create_clusters_to_terms_mapping import (
    create_clusters_to_terms_mapping,
)


def plot_node_treemap(
    params,
    nx_graph,
):
    """Creates a treemap.

    :meta private:
    """

    title = params.title_text

    node_occ = []
    node_color = []
    node_text = []
    parents = []

    clusters = create_clusters_to_terms_mapping(params=params, nx_graph=nx_graph)
    cluster_occ = {key: 0 for key in clusters}
    for key, names in clusters.items():
        for name in names:
            #
            # Extracs occurrences from node names. Example: 'regtech 10:100' -> 10
            occ = name.split(" ")[-1]
            occ = occ.split(":")[0]
            occ = float(occ)
            node_occ.append(occ)

            cluster_occ[key] += occ

            #
            # Uses the same color of clusters
            node_color.append(nx_graph.nodes[name]["node_color"])

            #
            # Sets text to node names without metrics
            node_name = name
            node_name = node_name.split(" ")[:-1]
            node_name = " ".join(node_name)

            node_text.append(node_name)
            parents.append(key)

    node_occ = [cluster_occ[key] * 0 for key in clusters] + node_occ
    node_color = ["lightgrey"] * len(clusters) + node_color
    node_text = list(clusters.keys()) + node_text
    parents = [""] * len(clusters) + parents

    fig = go.Figure()
    fig.add_trace(
        go.Treemap(
            labels=node_text,
            # parents=[""] * len(node_text),
            parents=parents,
            values=node_occ,
            textinfo="label+value+percent entry",
            opacity=0.9,
        )
    )
    fig.update_traces(marker={"cornerradius": 5})
    fig.update_layout(
        showlegend=False,
        margin={"t": 30, "l": 0, "r": 0, "b": 0},
        title=title if title is not None else "",
    )

    #
    # Change the colors of the treemap white
    fig.update_traces(
        #    marker={"line": {"color": "darkslategray", "width": 1}},
        marker_colors=node_color,
    )

    #
    # Change the font size of the labels
    fig.update_traces(textfont_size=12)

    return fig
