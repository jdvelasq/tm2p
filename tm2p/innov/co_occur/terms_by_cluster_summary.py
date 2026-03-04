"""
Terms by Cluster Summary
===============================================================================


Smoke tests:
    >>> from tm2p.analyze.experimental.co_occurrence import TermsByClusterSummary
    >>> df = (
    ...     TermsByClusterSummary()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # NETWORK:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     .using_association_index("association")
    ...     .using_minimum_terms_in_cluster(5)
    ...     .using_minimum_number_of_clusters(10)
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
    >>> df # doctest: +SKIP
       Cluster  ...                                              Terms
    0        0  ...  FINTECH 38:6131; THE_FINANCIAL_INDUSTRY 09:200...
    1        1  ...  TECHNOLOGIES 15:1633; FINANCIAL_TECHNOLOGIES 1...
    2        2  ...  THE_DEVELOPMENT 09:1293; INNOVATION 08:1816; T...
    3        3  ...  BANKS 08:1049; DATA 07:1086; CONSUMERS 07:0925...
    <BLANKLINE>
    [4 rows x 4 columns]


"""

from tm2p._intern import ParamsMixin
from tm2p.innov.co_occur.mixins import RecursiveClusteringMixin
from tm2p.synthes.netw.co_occur import (
    ItemsByClusterSummary as ClassicalTermsByClusterSummary,
)


class TermsByClusterSummary(
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
            ClassicalTermsByClusterSummary()
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
