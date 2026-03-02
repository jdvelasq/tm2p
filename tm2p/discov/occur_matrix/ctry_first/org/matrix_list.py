"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.ctry_first.org import MatrixList
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
                                             rows        columns  OCC
    0  SOUTHWEST UNIV FINANC ECON [CHN] 008:02269  CHN 039:08550    8
    1                    UNIV ZÜR [CHE] 007:00971  CHE 008:01458    7
    2                 PEKING UNIV [CHN] 004:00576  CHN 039:08550    4
    3              UNIV HONG KONG [HKG] 004:00760  HKG 004:01041    4
    4       FED RESERV BANK PHILA [USA] 005:01156  USA 019:05425    3
    5             HORIZ UNIV COLL [ARE] 003:00254  CHN 039:08550    3
    6               SHANGHAI UNIV [CHN] 003:00911  CHN 039:08550    3
    7               SOONGSIL UNIV [KOR] 003:00377  KOR 009:01264    3
    8    TASHKENT STATE UNIV ECON [UZB] 003:00254  CHN 039:08550    3
    9         XI'AN JIAOTONG UNIV [CHN] 003:00689  CHN 039:08550    3


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
