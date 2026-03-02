"""
Terms by Dimension Frane
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
## >>> from tm2p.packages.factor_analysis.tfidf import terms_by_dimension_frame
## >>> (
## ...     TermsByDimensionDataFrame()
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
## ...     ).build()
## ... ).head()



"""

import pandas as pd  # type: ignore

from tm2p.discov.tfidf._intern.matrix import Matrix as TfIdfDataFrame


def terms_by_dimension_frame(
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
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    matrix_values = TfIdfDataFrame(
        #
        # TF PARAMS:
        field=field,
        is_binary=is_binary,
        cooc_within=cooc_within,
        #
        # ITEM FILTERS:
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
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    ).T

    decomposition_estimator.fit(matrix_values)
    trans_matrix_values = decomposition_estimator.transform(matrix_values)

    embedding = pd.DataFrame(
        trans_matrix_values,
        index=matrix_values.index,
        columns=list(range(decomposition_estimator.n_components)),
    )
    embedding.columns.name = "dim"

    return embedding
