"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.authkw.org_first import MatrixList
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
    0                        UNIV ZÜR [CHE] 005:00659        fintech 117:25478    5
    1      SOUTHWEST UNIV FINANC ECON [CHN] 005:01236        fintech 117:25478    4
    2           FED RESERV BANK PHILA [USA] 003:00682        fintech 117:25478    3
    3               CAP UNIV ECON BUS [CHN] 002:00456        fintech 117:25478    2
    4                 CHANDIGARH UNIV [IND] 002:00183        fintech 117:25478    2
    5                   IMP COLL LOND [GBR] 002:00474        fintech 117:25478    2
    6                       LATV UNIV [LVA] 002:00273        fintech 117:25478    2
    7  MAULANA AZAD NATL INST TECHNOL [IND] 002:00256        fintech 117:25478    2
    8  MAULANA AZAD NATL INST TECHNOL [IND] 002:00256  green finance 011:02844    2
    9                       PACE UNIV [USA] 002:00511        fintech 117:25478    2


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
