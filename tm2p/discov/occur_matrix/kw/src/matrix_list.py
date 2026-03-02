"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.kw.src import MatrixList
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
    0  TECHNOL FORECAST SOC CHANG 006:01575                  fintech 119:26148    6
    1                RESOUR POLIC 007:01074                  finance 029:07137    5
    2                RESOUR POLIC 007:01074                  fintech 119:26148    5
    3                RESOUR POLIC 007:01074  sustainable development 015:02158    5
    4                EUR J FINANC 004:01002                  fintech 119:26148    4
    5                FINANC INNOV 005:00877                  fintech 119:26148    4
    6          RES INT BUS FINANC 004:00530                  fintech 119:26148    4
    7                RESOUR POLIC 007:01074                    china 018:03596    4
    8                RESOUR POLIC 007:01074           sustainability 013:02308    4
    9         IND MANAG DATA SYST 003:01154                  fintech 119:26148    3


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
