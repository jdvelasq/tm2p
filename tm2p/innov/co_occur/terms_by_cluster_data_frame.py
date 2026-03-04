"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.analyze.experimental.co_occurrence import TermsByClusterDataFrame
    >>> from tm2p.refine.thesaurus_old.descriptors import ApplyThesaurus, InitializeThesaurus

    >>> # Restore the column values to initial values
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Generate terms by cluster data frame
    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
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

    >>> # Display the resulting data frame
    >>> print(df.to_string()) # doctest: +SKIP
                                    0                               1                                        2                   3
    0                 FINTECH 38:6131            TECHNOLOGIES 15:1633                  THE_DEVELOPMENT 09:1293       BANKS 08:1049
    1  THE_FINANCIAL_INDUSTRY 09:2006  FINANCIAL_TECHNOLOGIES 12:1615                       INNOVATION 08:1816        DATA 07:1086
    2            PRACTITIONER 06:1194                 FINANCE 10:1188  THE_FINANCIAL_SERVICES_INDUSTRY 06:1237   CONSUMERS 07:0925
    3    THE_FINANCIAL_SECTOR 05:1147              REGULATORS 08:0974               FINANCIAL_SERVICES 06:1116  THE_IMPACT 06:0908
    4  INFORMATION_TECHNOLOGY 05:1101                   CHINA 06:0673                         SERVICES 06:1089
    5       FINTECH_COMPANIES 05:1072



"""

from tm2p._intern import ParamsMixin
from tm2p.innov.co_occur.mixins import RecursiveClusteringMixin
from tm2p.synthes.netw.co_occur import (
    ItemsByClusterDataFrame as ClassicalTermsByClusterDataFrame,
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
