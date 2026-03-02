"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.kw.pubtype import MatrixList
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
                    rows                            columns  OCC
    0  Article 142:32733                  fintech 119:26148  101
    1  Article 142:32733                  finance 029:07137   24
    2  Article 142:32733                    china 018:03596   17
    3  Article 142:32733               innovation 020:03916   16
    4  Article 142:32733      financial inclusion 017:03823   15
    5  Article 142:32733     financial technology 015:02583   13
    6  Article 142:32733                  banking 013:03043   11
    7  Article 142:32733  sustainable development 015:02158   11
    8  Article 142:32733           sustainability 013:02308    9
    9   Review 014:03303                  fintech 119:26148    7


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
