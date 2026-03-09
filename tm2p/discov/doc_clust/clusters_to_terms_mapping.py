"""
Clusters to Terms Mapping
===============================================================================


Smoke tests:
    >>> from sklearn.cluster import KMeans
    >>> kmeans = KMeans(
    ...     n_clusters=4,
    ...     init="k-means++",
    ...     n_init=10,
    ...     max_iter=300,
    ...     tol=0.0001,
    ...     algorithm="lloyd",
    ...     random_state=0,
    ... )
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.doc_clust import ClustersToTermsMapping
    >>> mapping = (
    ...     ClustersToTermsMapping()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.KW_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict(kmeans)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> import pprint
    >>> pprint.pprint(mapping)


"""

from tm2p._intern import ParamsMixin
from tm2p.discov.doc_clust.term_occurrence_by_cluster import TermOccurrenceByCluster


class ClustersToTermsMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        contingency_table = (
            TermOccurrenceByCluster().update(**self.params.__dict__).run()
        )

        themes = contingency_table.idxmax(axis=1)

        mapping = {}
        for word, theme in zip(themes.index, themes):
            if theme not in mapping:
                mapping[theme] = []
            mapping[theme].append(word)

        return mapping
