import graphviz

from tm2p._intern.nx.extract_communities import extract_communities
from tm2p._intern.nx.summarize_communities import summarize_communities


def concept_grid_plot(
    nx_graph,
    conserve_counters,
    n_head,
    fontsize,
):
    summary = summarize_communities(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        conserve_counters=True,
    )

    data_frame = extract_communities(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        conserve_counters=True,
    )

    if n_head is not None:
        data_frame = data_frame.head(n_head)

    graph = graphviz.Digraph(
        "graph",
        node_attr={"shape": "record"},
    )

    for i_cluster, col in enumerate(data_frame.columns):
        text = data_frame[col].to_list()
        if conserve_counters is False:
            text = [" ".join(str(t).split(" ")[:-1]) for t in text]
        text = [t if t != "" else "." for t in text]
        text = "\\r".join(text) + "\\r"
        cluster_name = (
            str(col) + " (" + str(summary.loc[i_cluster, "Percentage"]) + " %)"
        )
        graph.node(
            str(col),
            label=r"{" + cluster_name + "|" + text + r"}",
            fontsize=fontsize,
        )

    return graph
