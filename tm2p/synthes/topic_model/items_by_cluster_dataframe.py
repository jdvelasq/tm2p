"""
Terms by Cluster Frame
===============================================================================

Smoke tests:
    >>> from sklearn.decomposition import LatentDirichletAllocation
    >>> lda = LatentDirichletAllocation(
    ...     n_components=10,
    ...     learning_decay=0.7,
    ...     learning_offset=50.0,
    ...     max_iter=10,
    ...     batch_size=128,
    ...     evaluate_every=-1,
    ...     perp_tol=0.1,
    ...     mean_change_tol=0.001,
    ...     max_doc_update_iter=100,
    ...     random_state=0,
    ... )
    >>> from tm2p import ItemOrderBy, Field
    >>> from tm2p.synthes.topic_model import ItemsByClusterDataFrame
    >>> df = (
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
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_algorithm(lda)
    ...     .using_top_items_by_theme(5)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()
    cluster                               0  ...                                  9
    term                                     ...
    0                     fintech 155:33245  ...                  fintech 155:33245
    1                       china 033:06419  ...      financial inclusion 022:04623
    2             the development 026:05689  ...                  finance 050:10972
    3        financial technology 051:09258  ...  sustainable development 018:02898
    4                    evidence 018:03900  ...               innovation 033:07734
    <BLANKLINE>
    [5 rows x 10 columns]


"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.synthes.topic_model.cluster_to_items_mapping import ClusterToItemsMapping


class ItemsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        mapping = ClusterToItemsMapping().update(**self.params.__dict__).run()

        frame = pd.DataFrame.from_dict(mapping, orient="index").T
        frame = frame.fillna("")
        frame = frame.sort_index(axis=1)
        frame.columns.name = "cluster"
        frame.index.name = "term"
        return frame
