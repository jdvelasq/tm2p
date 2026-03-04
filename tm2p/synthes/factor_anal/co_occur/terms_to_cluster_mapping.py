"""
Terms to Cluster Mapping
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
## >>> from tm2p.packages.factor_analysis.co_occurrence import terms_to_cluster_mapping
## >>> mapping = (
## ...     TermsToClusterMapping()
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
## ...     # ASSOCIATION INDEX:
## ...     .using_association_index(None)
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
## >>> from pprint import pprint
## >>> pprint(mapping)



"""

from tm2p.synthes.factor_anal._intern.terms_to_cluster_mapping import (
    _terms_to_cluster_mapping,
)
from tm2p.synthes.factor_anal.co_occur.terms_by_dimension_data_frame import (
    terms_by_dimension_frame,
)


def terms_to_cluster_mapping(
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

    mapping = _terms_to_cluster_mapping(
        terms_by_dimmension=embedding,
        clustering_estimator_or_dict=clustering_estimator_or_dict,
    )

    return mapping
