"""
Terms by Cluster Frame
===============================================================================


Smoke tests:
    >>> from tm2p.packages.networks.citation.authors import TermsByClusterDataFrame

    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()

    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
                          0                    1                   2
    0      Gomber P. 2:1065     Hornuf L. 2:0358  Jagtiani J. 3:0317
    1  Kauffman R.J. 1:0576     Haddad C. 1:0258   Lemieux C. 2:0253
    2      Parker C. 1:0576  Puschmann T. 1:0253
    3     Weber B.W. 1:0576
    4     Koch J.-A. 1:0489

    >>> df = (
    ...     TermsByClusterDataFrame()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .having_items_in_top(30)
    ...     .using_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()

    >>> # Display the resulting data frame
    >>> print(df)  # doctest: +NORMALIZE_WHITESPACE
                   0             1            2
    0      Gomber P.     Hornuf L.  Jagtiani J.
    1  Kauffman R.J.     Haddad C.   Lemieux C.
    2      Parker C.  Puschmann T.
    3     Weber B.W.
    4     Koch J.-A.



"""

from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.from_others.terms_by_cluster_data_frame import (
    TermsByClusterDataFrame as OtherTermsByClusterDataFrame,
)


class TermsByClusterDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            OtherTermsByClusterDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .unit_of_analysis("authors")
            .run()
        )
