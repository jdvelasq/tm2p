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
    >>> from tm2p.packages.topic_modeling.user import TermsByClusterDataFrame
    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_field("raw_descriptors")
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DECOMPOSITION:
    ...     .using_decomposition_algorithm(lda)
    ...     .using_top_terms_by_theme(5)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_row_normalization(None)
    ...     .using_idf_reweighting(False)
    ...     .using_idf_weights_smoothing(False)
    ...     .using_sublinear_tf_scaling(False)
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
    >>> df.head() # doctest: +SKIP
    cluster                             0  ...                               9
    term                                   ...
    0                     FINTECH 38:6131  ...                 FINTECH 38:6131
    1        FINANCIAL_TECHNOLOGY 11:1519  ...  THE_FINANCIAL_INDUSTRY 09:2006
    2                  TECHNOLOGY 10:1220  ...                A_SURVEY 03:0484
    3                       BANKS 08:1049  ...           PRACTITIONERS 05:0992
    4                  REGULATORS 08:0974  ...               THE_FIELD 05:0834
    <BLANKLINE>
    [5 rows x 10 columns]


"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.synthes.topic_model.cluster_to_terms_mapping import ClusterToTermsMapping


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        mapping = ClusterToTermsMapping().update(**self.params.__dict__).run()

        frame = pd.DataFrame.from_dict(mapping, orient="index").T
        frame = frame.fillna("")
        frame = frame.sort_index(axis=1)
        frame.columns.name = "cluster"
        frame.index.name = "term"
        return frame
