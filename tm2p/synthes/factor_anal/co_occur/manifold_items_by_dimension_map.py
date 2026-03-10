"""
ManifoldItemsByDimensionMap
===============================================================================

Smoke test:
    >>> from sklearn.decomposition import PCA
    >>> pca = PCA(
    ...     n_components=5,
    ...     whiten=False,
    ...     svd_solver="auto",
    ...     tol=0.0,
    ...     iterated_power="auto",
    ...     n_oversamples=10,
    ...     power_iteration_normalizer="auto",
    ...     random_state=0,
    ... )
    >>> from sklearn.manifold import TSNE
    >>> tsne = TSNE(
    ...     perplexity=10.0,
    ...     early_exaggeration=12.0,
    ...     learning_rate="auto",
    ...     max_iter=1000,
    ...     n_iter_without_progress=300,
    ...     min_grad_norm=1e-07,
    ...     metric="euclidean",
    ...     metric_params=None,
    ...     init="pca",
    ...     verbose=0,
    ...     random_state=0,
    ...     method="barnes_hut",
    ...     angle=0.5,
    ...     n_jobs=None,
    ... )
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.factor_anal.co_occur import ManifoldItemsByDimensionMap
    >>> plot = (
    ...     ManifoldItemsByDimensionMap()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_estimator(pca)
    ...     #
    ...     # MANIFOLD:
    ...     .using_manifold_estimator(tsne)
    ...     #
    ...     # ASSOCIATION INDEX:
    ...     .using_association_index(None)
    ...     #
    ...     # MAP:
    ...     .using_node_colors(["#465c6b"])
    ...     .using_node_size(10)
    ...     .using_textfont_size(8)
    ...     .using_textfont_color("#465c6b")
    ...     #
    ...     .using_xaxes_range(None, None)
    ...     .using_yaxes_range(None, None)
    ...     .using_axes_visible(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> plot.write_html("docsrc/_generated/px.packages.factor_analysis/co_occurrence/manifold_terms_by_dimension_map.html")

.. raw:: html

    <iframe src="../_generated/px.packages.factor_analysis/co_occurrence/manifold_terms_by_dimension_map.html"
    height="800px" width="100%" frameBorder="0"></iframe>


"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.factor_anal._intern.manifold_2d_map import manifold_2d_map
from tm2p.synthes.factor_anal.co_occur.items_by_dimension_data_frame import (
    terms_by_dimension_frame,
)


class ManifoldItemsByDimensionMap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        pass


def manifold_terms_by_dimension_map(
    #
    # PARAMS:
    field,
    association_index=None,
    #
    # TERM PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_terms=None,
    #
    # DECOMPOSITION:
    decomposition_estimator=None,
    #
    # MANIFOLD PARAMS:
    manifold_estimator=None,
    #
    # MAP PARAMS:
    node_color="#465c6b",
    node_size=10,
    textfont_size=8,
    textfont_color="#465c6b",
    xaxes_range=None,
    yaxes_range=None,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    embedding = terms_by_dimension_frame(
        #
        # FUNCTION PARAMS:
        field=field,
        association_index=association_index,
        #
        # TERM PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_terms=custom_terms,
        #
        # DECOMPOSITION:
        decomposition_estimator=decomposition_estimator,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    manifold = manifold_estimator.fit_transform(embedding)

    return manifold_2d_map(
        node_x=manifold[:, 0],
        node_y=manifold[:, 1],
        node_text=embedding.index.to_list(),
        node_color=node_color,
        node_size=node_size,
        title_x="Dim 0",
        title_y="Dim 1",
        textfont_size=textfont_size,
        textfont_color=textfont_color,
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
    )


#
