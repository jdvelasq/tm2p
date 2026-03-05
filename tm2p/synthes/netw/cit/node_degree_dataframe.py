"""
NodeDegreeDataFrame
===============================================================================

Smoke tests:
    >>> from tm2p import CitationUnit
    >>> from tm2p.synthes.netw.cit import NodeDegreeDataFrame
    >>> (
    ...     NodeDegreeDataFrame()
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
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()
       NODE                                               NAME  DEGREE
    0     0  Anagnostopoulos, 2018, J ECON BUS, V100, P7 1:...       3
    1     1                    Hu, 2019, SYMMETRY, V11 1:00425       2
    2     2  Arner, 2017, NORTHWEST J INT LAW BUS, V37, P37...       2
    3     3         Gabor, 2017, POLIT ECON, V22, P423 1:00563       1
    4     4  Arner, 2020, EUR BUS ORGAN LAW REV, V21, P7 1:...       1


    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # CITATION UNIT:
    ...     .with_citation_unit(CitationUnit.DOC)
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
    ... ).head()
       NODE                                             NAME  DEGREE
    0     0      Anagnostopoulos, 2018, J ECON BUS, V100, P7       3
    1     1                          Hu, 2019, SYMMETRY, V11       2
    2     2  Arner, 2017, NORTHWEST J INT LAW BUS, V37, P373       2
    3     3               Gabor, 2017, POLIT ECON, V22, P423       1
    4     4      Arner, 2020, EUR BUS ORGAN LAW REV, V21, P7       1


    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # CITATION UNIT:
    ...     .with_citation_unit(CitationUnit.CTRY)
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
    ... ).head()
       NODE           NAME  DEGREE
    0     0  CHN 045:09715      22
    1     1  AUS 014:03468      16
    2     2  DEU 013:05295      16
    3     3  FRA 011:02475      15
    4     4  GBR 033:06802      14


    >>> (
    ...     NodeDegreeDataFrame()
    ...     #
    ...     # CITATION UNIT:
    ...     .with_citation_unit(CitationUnit.CTRY)
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
    ... ).head()
       NODE NAME  DEGREE
    0     0  CHN      22
    1     1  AUS      16
    2     2  DEU      16
    3     3  FRA      15
    4     4  GBR      14

"""

from tm2p import CitationUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.cit._intern.doc import (
    NodeDegreeDataFrame as DocNodeDegreeDataFrame,
)
from tm2p.synthes.netw.cit._intern.other import (
    NodeDegreeDataFrame as OtherNodeDegreeDataFrame,
)


class NodeDegreeDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.citation_unit == CitationUnit.DOC:
            NodeDegree = DocNodeDegreeDataFrame
        else:
            NodeDegree = OtherNodeDegreeDataFrame

        return (
            NodeDegree()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )
