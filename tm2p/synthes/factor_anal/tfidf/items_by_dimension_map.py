"""
ItemsByDimensionMap
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
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.factor_anal.tfidf import ItemsByDimensionMap
    >>> plot = (
    ...     ItemsByDimensionMap()
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
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
    ...     #
    ...     # MAP:
    ...     .using_plot_dimensions(0, 1)
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
    >>> plot.write_html("docsrc/__static/factor_analysis/tfidf/terms_by_dimension_map.html")

.. raw:: html

    <iframe src="../../_static/factor_analysis/tfidf/terms_by_dimension_map.html"
    height="600px" width="100%" frameBorder="0"></iframe>

"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.factor_anal._intern.manifold_2d_map import manifold_2d_map
from tm2p.synthes.factor_anal.tfidf.items_by_dimension_dataframe import (
    terms_by_dimension_frame,
)


class ItemsByDimensionMap(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        pass


def terms_by_dimension_map(
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
    # MAP PARAMS:
    dim_x=0,
    dim_y=1,
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
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    return manifold_2d_map(
        node_x=embedding[dim_x],
        node_y=embedding[dim_y],
        node_text=embedding.index.to_list(),
        node_color=node_color,
        node_size=node_size,
        title_x=dim_x,
        title_y=dim_y,
        textfont_size=textfont_size,
        textfont_color=textfont_color,
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
    )
