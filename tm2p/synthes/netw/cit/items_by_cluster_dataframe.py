"""
ItemsByClusterDataFrame
===============================================================================


Smoke tests:
    >>> from tm2p import CitationUnit
    >>> from tm2p.synthes.netw.cit import ItemsByClusterDataFrame
    >>> df = (
    ...     ItemsByClusterDataFrame()
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
                                                       0  ...                                                  3
    0  Arner, 2020, EUR BUS ORGAN LAW REV, V21, P7 1:...  ...         Bollaert, 2021, J CORP FINANC, V68 1:00393
    1                Zhou, 2022, ECOL ECON, V193 1:00507  ...  Tao, 2022, TECHNOL FORECAST SOC CHANG, V174 1:...
    2  Anagnostopoulos, 2018, J ECON BUS, V100, P7 1:...  ...
    3  Arner, 2017, NORTHWEST J INT LAW BUS, V37, P37...  ...
    4       Cheng, 2020, PAC BASIN FINANC J, V63 1:00363  ...
    <BLANKLINE>
    [5 rows x 4 columns]


    >>> df = (
    ...     ItemsByClusterDataFrame()
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
                                                     0  ...                                            3
    0      Arner, 2020, EUR BUS ORGAN LAW REV, V21, P7  ...           Bollaert, 2021, J CORP FINANC, V68
    1                      Zhou, 2022, ECOL ECON, V193  ...  Tao, 2022, TECHNOL FORECAST SOC CHANG, V174
    2      Anagnostopoulos, 2018, J ECON BUS, V100, P7  ...
    3  Arner, 2017, NORTHWEST J INT LAW BUS, V37, P373  ...
    4             Cheng, 2020, PAC BASIN FINANC J, V63  ...
    <BLANKLINE>
    [5 rows x 4 columns]


    >>> df = (
    ...     ItemsByClusterDataFrame()
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
                             0                           1                       2
    0      Dolata M. 003:00330       Jagtiani J. 005:01156    Arner D.W. 003:00911
    1     Schwabe G. 003:00330  Schwienbacher A. 002:00611   Barberis J. 003:00445
    2  Zavolokina L. 003:00330          Allen F. 002:00474  Buckley R.P. 002:00898
    3        Chen L. 002:00579             Gu X. 002:00474
    4         Gai K. 002:00511           Wang Y. 002:00456


    >>> df = (
    ...     ItemsByClusterDataFrame()
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
                   0                 1             2
    0      Dolata M.       Jagtiani J.    Arner D.W.
    1     Schwabe G.  Schwienbacher A.   Barberis J.
    2  Zavolokina L.          Allen F.  Buckley R.P.
    3        Chen L.             Gu X.
    4         Gai K.           Wang Y.



"""

from tm2p import CitationUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.doc import (
    ItemsByClusterDataFrame as DocItemsByClusterDataFrame,
)
from tm2p.synthes.netw.cit._intern.other import (
    ItemsByClusterDataFrame as OtherItemsByClusterDataFrame,
)


class ItemsByClusterDataFrame(
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
