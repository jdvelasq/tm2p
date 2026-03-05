"""
ItemsByDimensionDataFrame
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
    >>> from tm2p.synthes.factor_anal.co_occur import ItemsByDimensionDataFrame
    >>> (
    ...     ItemsByDimensionDataFrame()
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
    ...     # ASSOCIATION INDEX:
    ...     .using_association_index(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()



"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.co_occur._intern.comput_assoc_index import comput_assoc_index


class ItemsByDimensionDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        pass


def terms_by_dimension_frame(
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
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    matrix_values = co_occurrence_matrix(
        #
        # FUNCTION PARAMS:
        columns=field,
        #
        # COLUMN PARAMS:
        col_top_n=top_n,
        col_occ_range=occ_range,
        col_gc_range=gc_range,
        col_custom_terms=custom_terms,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    matrix_values = comput_assoc_index(matrix_values, association_index)
    decomposition_estimator.fit(matrix_values)
    trans_matrix_values = decomposition_estimator.transform(matrix_values)

    embedding = pd.DataFrame(
        trans_matrix_values,
        index=matrix_values.index,
        columns=list(range(decomposition_estimator.n_components)),
    )
    embedding.columns.name = "dim"

    return embedding
