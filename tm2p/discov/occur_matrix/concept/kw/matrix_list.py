"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.concept.kw import MatrixList
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
                       rows                         columns  OCC
    0     fintech 119:26148               fintech 155:33245  119
    1     fintech 119:26148  financial technology 051:09258   32
    2     finance 029:07137               finance 050:10972   29
    3     fintech 119:26148               finance 050:10972   29
    4     finance 029:07137               fintech 155:33245   23
    5     fintech 119:26148                 banks 029:06252   23
    6     fintech 119:26148            innovation 033:07734   22
    7     fintech 119:26148                 china 033:06419   20
    8     fintech 119:26148    financial services 030:06887   20
    9  innovation 020:03916            innovation 033:07734   20


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
