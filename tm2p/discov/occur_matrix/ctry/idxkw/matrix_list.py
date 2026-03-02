"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.ctry.idxkw import MatrixList
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
    0                  finance 028:07080  CHN 045:09715   15
    1  sustainable development 017:02470  CHN 045:09715   11
    2                    china 010:02031  CHN 045:09715    9
    3                  fintech 024:05279  CHN 045:09715    7
    4               innovation 014:02604  CHN 045:09715    7
    5     economic development 008:02384  CHN 045:09715    5
    6       empirical analysis 006:00978  CHN 045:09715    5
    7                  fintech 024:05279  GBR 033:06802    5
    8            green economy 006:01076  CHN 045:09715    5
    9           sustainability 010:01546  CHN 045:09715    5


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
