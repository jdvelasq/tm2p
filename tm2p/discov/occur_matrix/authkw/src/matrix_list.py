"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.authkw.src import MatrixList
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
                                       rows            columns  OCC
    0  TECHNOL FORECAST SOC CHANG 006:01575  fintech 117:25478    6
    1                RESOUR POLIC 007:01074  fintech 117:25478    5
    2                EUR J FINANC 004:01002  fintech 117:25478    4
    3                FINANC INNOV 005:00877  fintech 117:25478    4
    4          RES INT BUS FINANC 004:00530  fintech 117:25478    4
    5         INT REV FINANC ANAL 005:00992  fintech 117:25478    3
    6                  J ECON BUS 003:00886  fintech 117:25478    3
    7       SUSTAIN (SWITZERLAND) 004:00741  fintech 117:25478    3
    8  ASIA-PACIFIC J FINANC STUD 002:00214  fintech 117:25478    2
    9                    BUS ECON 002:00748  fintech 117:25478    2


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
