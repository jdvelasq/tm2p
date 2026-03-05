"""
ItemsByClusterDataFrame
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
    >>> from sklearn.cluster import KMeans
    >>> kmeans = KMeans(
    ...     n_clusters=6,
    ...     init="k-means++",
    ...     n_init=10,
    ...     max_iter=300,
    ...     tol=0.0001,
    ...     algorithm="elkan",
    ...     random_state=0,
    ... )
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.factor_anal.co_occur import ItemsByClusterDataFrame
    >>> (
    ...     ItemsByClusterDataFrame()
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
    ...     # CLUSTERING:
    ...     .using_clustering_estimator_or_dict(kmeans)
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
from tm2p.synthes.factor_anal.co_occur.cluster_to_items_mapping import (
    cluster_to_terms_mapping,
)


class ItemsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        pass


def terms_by_cluster_frame(
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

    c2t_mapping = cluster_to_terms_mapping(
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

    frame = pd.DataFrame.from_dict(c2t_mapping, orient="index").T
    frame = frame.fillna("")
    frame = frame.sort_index(axis=1)

    return frame

    return frame
