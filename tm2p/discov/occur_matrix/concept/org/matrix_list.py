"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.concept.org import MatrixList
    >>> df = (
    ...     MatrixList()
    ...     #
    ...     # COLUMNS:
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .having_index_items_in_top(None)
    ...     .having_index_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_index_item_occurrences_between(2, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 1
    True
    >>> df.shape[1] > 1
    True
    >>> df.head(10)
                                             rows                    columns  OCC
    0  SOUTHWEST UNIV FINANC ECON [CHN] 008:02269          fintech 155:33245    8
    1                    UNIV ZÜR [CHE] 007:00971          fintech 155:33245    7
    2       FED RESERV BANK PHILA [USA] 005:01156          fintech 155:33245    5
    3  SOUTHWEST UNIV FINANC ECON [CHN] 008:02269            banks 029:06252    5
    4  SOUTHWEST UNIV FINANC ECON [CHN] 008:02269  the development 026:05689    5
    5                   LATV UNIV [LVA] 004:00456          fintech 155:33245    4
    6  SOUTHWEST UNIV FINANC ECON [CHN] 008:02269       innovation 033:07734    4
    7              UNIV HONG KONG [HKG] 004:00760          fintech 155:33245    4
    8          ADAM SMITH BUS SCH [GBR] 003:00398          fintech 155:33245    3
    9             HORIZ UNIV COLL [ARE] 003:00254            china 033:06419    3


"""

from tm2p._intern import ParamsMixin

from ..._intern import MatrixList as BaseMatrixList
from .._column import COLUMN_FIELD
from ._index import INDEX_FIELD


class MatrixList(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return (
            BaseMatrixList()
            .with_params(self.params)
            .with_column_field(COLUMN_FIELD)
            .with_index_field(INDEX_FIELD)
            .run()
        )
