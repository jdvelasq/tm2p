"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.auth_first.src import MatrixList
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
                                       rows                  columns  OCC
    0                  J ECON BUS 003:00886    Jagtiani J. 003:00682    2
    1               STRATEG CHANG 002:00372       Ashta A. 002:00372    2
    2                FINANC INNOV 005:00877     Muganyi T. 002:00656    1
    3                FINANC INNOV 005:00877  Zavolokina L. 003:00330    1
    4                FINANC MANAG 002:00376    Jagtiani J. 003:00682    1
    5          J INT MONEY FINANC 002:00572       Allen F. 002:00474    1
    6            J MANAG INF SYST 002:01611      Gomber P. 002:02579    1
    7                RENEW ENERGY 002:00340    Nenavath S. 002:00256    1
    8  ASIA-PACIFIC J FINANC STUD 002:00214       Allen F. 002:00474    0
    9  ASIA-PACIFIC J FINANC STUD 002:00214     Arner D.W. 002:00898    0


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
