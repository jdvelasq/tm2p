"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.auth.src import MatrixList
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
    0                  BUS ECON 002:00748      Hornuf L. 003:00904    2
    1                J ECON BUS 003:00886    Jagtiani J. 005:01156    2
    2                 ECON WIND 002:00044     Arner D.W. 003:00911    1
    3                 ECON WIND 002:00044    Barberis J. 003:00445    1
    4  ELECTRON COMMER RES APPL 002:00154  Kauffman R.J. 002:01445    1
    5              FINANC INNOV 005:00877      Dolata M. 003:00330    1
    6              FINANC INNOV 005:00877     Schwabe G. 003:00330    1
    7              FINANC INNOV 005:00877  Zavolokina L. 003:00330    1
    8              FINANC MANAG 002:00376    Jagtiani J. 005:01156    1
    9       INT REV ECON FINANC 002:00500          Li X. 003:00894    1


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
