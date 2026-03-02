"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.authkw.ctry_first import MatrixList
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
                rows                        columns  OCC
    0  CHN 039:08550              fintech 117:25478   24
    1  GBR 017:03919              fintech 117:25478   12
    2  USA 019:05425              fintech 117:25478   11
    3  IND 011:01471              fintech 117:25478    9
    4  CHE 008:01458              fintech 117:25478    7
    5  CHN 039:08550                china 009:01947    6
    6  GBR 017:03919  financial inclusion 017:03823    6
    7  KOR 009:01264              fintech 117:25478    6
    8  AUS 009:01749              fintech 117:25478    5
    9  CHN 039:08550        green finance 011:02844    5


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
