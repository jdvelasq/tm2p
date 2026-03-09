"""
ItemsByCluster
===============================================================================


Smoke tests:
    >>> from tm2p import CitationUnit
    >>> from tm2p.synthes.netw.cit import ItemsByCluster
    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # CITATION UNIT:
    ...     .with_citation_unit(CitationUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE


    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .with_citation_unit(CitationUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE


    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # ANALYSIS UNIT:
    ...     .with_citation_unit(CitationUnit.AUTH)
    ...     .having_items_in_top(30)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE


    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # UNIT OF ANALYSIS:
    ...     .with_citation_unit(CitationUnit.AUTH)
    ...     .having_items_in_top(30)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE


"""

from tm2p import CitationUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.doc import (
    ItemsByClusterDataFrame as DocItemsByClusterDataFrame,
)
from tm2p.synthes.netw.cit._intern.other import (
    ItemsByClusterDataFrame as OtherItemsByClusterDataFrame,
)


class ItemsByCluster(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.citation_unit == CitationUnit.DOC:
            ItemsByCluster = DocItemsByClusterDataFrame
        else:
            ItemsByCluster = OtherItemsByClusterDataFrame

        return (
            ItemsByCluster()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )
