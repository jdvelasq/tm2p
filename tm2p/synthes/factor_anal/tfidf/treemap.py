"""
Treemap
===============================================================================

## >>> from sklearn.decomposition import PCA
## >>> pca = PCA(
## ...     n_components=5,
## ...     whiten=False,
## ...     svd_solver="auto",
## ...     tol=0.0,
## ...     iterated_power="auto",
## ...     n_oversamples=10,
## ...     power_iteration_normalizer="auto",
## ...     random_state=0,
## ... )
## >>> from sklearn.cluster import KMeans
## >>> kmeans = KMeans(
## ...     n_clusters=6,
## ...     init="k-means++",
## ...     n_init=10,
## ...     max_iter=300,
## ...     tol=0.0001,
## ...     algorithm="elkan",
## ...     random_state=0,
## ... )
## >>> from tm2p.packages.factor_analysis.tfidf import treemap
## >>> plot = (
## ...     Treemap()
## ...     #
## ...     # FIELD:
## ...     .with_field("descriptors")
## ...     .having_items_in_top(50)
## ...     .having_items_ordered_by("OCC")
## ...     .having_item_occurrences_between(None, None)
## ...     .having_item_citations_between(None, None)
## ...     .having_items_in(None)
## ...     #
## ...     # DECOMPOSITION:
## ...     .using_decomposition_estimator(pca)
## ...     #
## ...     # CLUSTERING:
## ...     .using_clustering_estimator_or_dict(kmeans)
## ...     #
## ...     # TFIDF:
## ...     .using_binary_item_frequencies(False)
## ...     .using_row_normalization(None)
## ...     .using_idf_reweighting(False)
## ...     .using_idf_weights_smoothing(False)
## ...     .using_sublinear_tf_scaling(False)
## ...     #
## ...     # DATABASE:
## ...     .where_root_directory("tests/fintech/")
## ...     .where_database("main")
## ...     .where_record_years_range(None, None)
## ...     .where_record_citations_range(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .run()
## ... )
## >>> plot.write_html("docsrc/_generated/px.packages.factor_analysis/tfidf/treemap.html")

.. raw:: html

    <iframe src="../_generated/px.packages.factor_analysis/tfidf/treemap.html"
    height="800px" width="100%" frameBorder="0"></iframe>



"""

import plotly.express as px  # type: ignore
import plotly.graph_objs as go  # type: ignore

from tm2p.synthes.factor_anal.tfidf.terms_to_cluster_mapping import (
    terms_to_cluster_mapping,
)

CLUSTER_COLORS = (
    px.colors.qualitative.Dark24
    + px.colors.qualitative.Light24
    + px.colors.qualitative.Pastel1
    + px.colors.qualitative.Pastel2
    + px.colors.qualitative.Set1
    + px.colors.qualitative.Set2
    + px.colors.qualitative.Set3
)


def treemap(
    #
    # PARAMS:
    field,
    #
    # TF PARAMS:
    is_binary: bool = True,
    cooc_within: int = 1,
    #
    # TERM PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_terms=None,
    #
    # TF-IDF parameters:
    norm=None,
    use_idf=False,
    smooth_idf=False,
    sublinear_tf=False,
    #
    # DECOMPOSITION:
    decomposition_estimator=None,
    #
    # CLUSTERING:
    clustering_estimator_or_dict=None,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    c2t_mapping = terms_to_cluster_mapping(
        #
        # FUNCTION PARAMS:
        field=field,
        #
        # TF PARAMS:
        is_binary=is_binary,
        cooc_within=cooc_within,
        #
        # TERM PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_terms=custom_terms,
        #
        # TF-IDF parameters:
        norm=norm,
        use_idf=use_idf,
        smooth_idf=smooth_idf,
        sublinear_tf=sublinear_tf,
        #
        # DECOMPOSITION:
        decomposition_estimator=decomposition_estimator,
        #
        # CLUSTERING:
        clustering_estimator_or_dict=clustering_estimator_or_dict,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    node_occ = []
    node_color = []
    node_text = []
    parents = []

    name2color = {
        term: CLUSTER_COLORS[cluster] for term, cluster in c2t_mapping.items()
    }

    clusters = list(set(c2t_mapping.values()))
    cluster_occ = {key: 0 for key in clusters}

    for term, cluster in c2t_mapping.items():
        #
        # Extracs occurrences from node names. Example: 'regtech 10:100' -> 10
        occ = term.split(" ")[-1]
        occ = occ.split(":")[0]
        occ = float(occ)
        node_occ.append(occ)
        cluster_occ[cluster] += occ

        #
        # Uses the same color of clusters
        node_color.append(name2color[term])

        #
        # Sets text to node names without metrics
        node_name = term
        node_name = node_name.split(" ")[:-1]
        node_name = " ".join(node_name)

        node_text.append(node_name)
        parents.append(cluster)

    node_occ = [cluster_occ[key] * 0 for key in clusters] + node_occ
    node_color = ["lightgrey"] * len(clusters) + node_color
    node_text = clusters + node_text
    parents = [""] * len(clusters) + parents

    fig = go.Figure()
    fig.add_trace(
        go.Treemap(
            labels=node_text,
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

    return fig
