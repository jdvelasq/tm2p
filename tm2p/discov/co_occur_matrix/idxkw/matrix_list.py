"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.co_occur_matrix.idxkw import MatrixList
    >>> df = (
    ...     MatrixList()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
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
                                    rows                            columns  OCC
    0                  finance 028:07080                  finance 028:07080   30
    1  sustainable development 017:02470  sustainable development 017:02470   25
    2                  fintech 024:05279                  fintech 024:05279   24
    3               innovation 014:02604               innovation 014:02604   16
    4     economic development 008:02384     economic development 008:02384   14
    5                  finance 028:07080  sustainable development 017:02470   11
    6  sustainable development 017:02470                  finance 028:07080   11
    7                    china 010:02031                    china 010:02031   10
    8               innovation 014:02604  sustainable development 017:02470   10
    9           sustainability 010:01546           sustainability 010:01546   10


"""

from tm2p._intern import ParamsMixin

from ...occur_matrix._intern.matrix_list import MatrixList as BaseMatrixList
from ._field import SOURCE_FIELD


class MatrixList(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return (
            BaseMatrixList()
            .update(**self.params.__dict__)
            #
            # COLUMNS:
            .with_column_field(SOURCE_FIELD)
            .having_column_items_in_top(self.params.top_n)
            .having_column_items_ordered_by(self.params.items_order_by)
            .having_column_item_occurrences_between(
                self.params.item_occurrences_range[0],
                self.params.item_occurrences_range[1],
            )
            .having_column_item_citations_between(
                self.params.item_citations_range[0],
                self.params.item_citations_range[1],
            )
            .having_column_items_in(self.params.items_in)
            #
            # ROWS:
            .with_index_field(SOURCE_FIELD)
            .having_index_items_in_top(self.params.top_n)
            .having_index_items_ordered_by(self.params.items_order_by)
            .having_index_item_occurrences_between(
                self.params.item_occurrences_range[0],
                self.params.item_occurrences_range[1],
            )
            .having_index_item_citations_between(
                self.params.item_citations_range[0],
                self.params.item_citations_range[1],
            )
            .having_index_items_in(self.params.items_in)
            #
            .run()
        )
