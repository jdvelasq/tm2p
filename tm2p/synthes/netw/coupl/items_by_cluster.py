"""
ItemsByCluster
===============================================================================

Smoke tests:
    >>> from tm2p import CouplingUnit
    >>> from tm2p.synthes.netw.coupl import ItemsByCluster
    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
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
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
                                             0  ...                                                5
    0         Gomber, 2017, J BUS ECON 1:01152  ...            Jünger, 2020, FINANC RES LETT 1:00256
    1           Haddad, 2019, BUS ECON 1:00530  ...  Lim, 2019, INT J HUMANCOMPUTER INTERACT 1:00254
    2        Demir, 2022, EUR J FINANC 1:00528  ...
    3    Bollaert, 2021, J CORP FINANC 1:00393  ...
    4  Allen, 2022, J INT MONEY FINANC 1:00256  ...
    <BLANKLINE>
    [5 rows x 6 columns]

    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
                                     0  ...                                        5
    0         Gomber, 2017, J BUS ECON  ...            Jünger, 2020, FINANC RES LETT
    1           Haddad, 2019, BUS ECON  ...  Lim, 2019, INT J HUMANCOMPUTER INTERACT
    2        Demir, 2022, EUR J FINANC  ...
    3    Bollaert, 2021, J CORP FINANC  ...
    4  Allen, 2022, J INT MONEY FINANC  ...
    <BLANKLINE>
    [5 rows x 6 columns]

    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.AUTH)
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
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
                         0  ...                       4
    0      Li X. 003:00894  ...    Arner D.W. 003:00911
    1  Lee C.-C. 002:00717  ...  Buckley R.P. 002:00898
    2   Yu C.-H. 002:00717  ...
    3    Zhao J. 002:00717  ...
    4     Luo S. 002:00670  ...
    <BLANKLINE>
    [5 rows x 5 columns]

    >>> df = (
    ...     ItemsByCluster()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.AUTH)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
               0                 1            2              3             4
    0      Li X.         Hornuf L.  Jagtiani J.      Dolata M.    Arner D.W.
    1  Lee C.-C.         Gomber P.     Allen F.     Schwabe G.  Buckley R.P.
    2   Yu C.-H.  Schwienbacher A.        Gu X.  Zavolokina L.
    3    Zhao J.            Liu J.
    4     Luo S.


"""

from tm2p import CouplingUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.doc import (
    ItemsByClusterDataFrame as DocItemsByClusterDataFrame,
)
from tm2p.synthes.netw.coupl._intern.other import (
    ItemsByClusterDataFrame as OtherItemsByClusterDataFrame,
)


class ItemsByCluster(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.coupling_unit == CouplingUnit.DOC:
            ItemsByCluster = DocItemsByClusterDataFrame
        else:
            ItemsByCluster = OtherItemsByClusterDataFrame

        return (
            ItemsByCluster()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )
