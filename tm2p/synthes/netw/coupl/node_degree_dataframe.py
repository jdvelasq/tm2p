"""
Network Degree Frame
===============================================================================

Smoke tests:
    >>> from tm2p import CouplingUnit
    >>> from tm2p.synthes.netw.coupl import NodeDegreeDataFrame
    >>> df = (
    ...     NodeDegreeDataFrame()
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
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
       NODE                                         NAME  DEGREE
    0     0        Bollaert, 2021, J CORP FINANC 1:00393       4
    1     1            Cai, 2018, ACCOUNT FINANC 1:00251       4
    2     2             Gomber, 2017, J BUS ECON 1:01152       3
    3     3               Haddad, 2019, BUS ECON 1:00530       3
    4     4  Belanche, 2019, IND MANAG DATA SYST 1:00605       2

    >>> df = (
    ...     NodeDegreeDataFrame()
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
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
       NODE                                 NAME  DEGREE
    0     0        Bollaert, 2021, J CORP FINANC       4
    1     1            Cai, 2018, ACCOUNT FINANC       4
    2     2             Gomber, 2017, J BUS ECON       3
    3     3               Haddad, 2019, BUS ECON       3
    4     4  Belanche, 2019, IND MANAG DATA SYST       2


    >>> df = (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.CTRY)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
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
       NODE           NAME  DEGREE
    0     0  CHN 045:09715      24
    1     1  GBR 033:06802      17
    2     2  USA 031:09562      17
    3     3  FRA 011:02475      17
    4     4  SAU 007:00748      17

    >>> df = (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.CTRY)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
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
       NODE NAME  DEGREE
    0     0  CHN      24
    1     1  GBR      17
    2     2  USA      17
    3     3  FRA      17
    4     4  SAU      17

"""

from tm2p import CouplingUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.doc import (
    NodeDegreeDataFrame as DocNodeDegreeDataFrame,
)
from tm2p.synthes.netw.coupl._intern.other import (
    NodeDegreeDataFrame as OtherNodeDegreeDataFrame,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.coupling_unit == CouplingUnit.DOC:
            NodeDegree = DocNodeDegreeDataFrame
        else:
            NodeDegree = OtherNodeDegreeDataFrame

        return (
            NodeDegree()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )
