"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.analyze.experimental.emergence import TermsByClusterDataFrame
    >>> from tm2p.refine.thesaurus_old.descriptors import ApplyThesaurus, InitializeThesaurus

    >>> # Restore the column values to initial values
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Generate terms by cluster data frame
    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # EMERGENCE:
    ...     .using_baseline_periods(3)
    ...     .using_recent_periods(3)
    ...     .using_novelty_threshold(0.15)
    ...     .using_total_records_threshold(7)
    ...     .using_periods_with_at_least_one_record(3)
    ...     .using_ratio_threshold(0.5)
    ...     .using_minimum_terms_in_cluster(5)
    ...     #
    ...     # NETWORK:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     .using_association_index("association")
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

    >>> # Display the resulting data frame
    >>> print(df.to_string()) # doctest: +NORMALIZE_WHITESPACE +SKIP
                                    0
    0  FINANCIAL_TECHNOLOGIES 12:1615
    1                   BANKS 08:1049
    2                    DATA 07:1086
    3               CONSUMERS 07:0925




"""

from tm2p._intern import ParamsMixin
from tm2p.innov.emerg.mixins import RecursiveClusteringMixin
from tm2p.synthes.netw.co_occur import (
    ItemsByCluster as ClassicalTermsByClusterDataFrame,
)


class TermsByClusterDataFrame(
    ParamsMixin,
    RecursiveClusteringMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):
        pass

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:
            pass

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__build_final_dataframe(self):

        equivalence = {t.split(" ")[0]: t for t in self.terms_with_metrics}
        mapping = {}

        for i, terms in enumerate(self.discovered_clusters):
            for term in terms:
                key = equivalence[term]
                mapping[key] = i

        self.data_frame = (
            ClassicalTermsByClusterDataFrame()
            .update(**self.params.__dict__)
            #
            .using_clustering_algorithm_or_dict(mapping)
            #
            .having_items_in_top(None)
            .having_items_ordered_by("OCC")
            .having_item_occurrences_between(None, None)
            .having_item_citations_between(None, None)
            .having_items_in(self.selected_terms)
            #
            .run()
        )

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self.internal__notify_process_start()
        self.internal__computer_recursive_clusters()
        self.internal__build_final_dataframe()
        self.internal__notify_process_end()

        return self.data_frame


#
