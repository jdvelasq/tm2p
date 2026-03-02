"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.auth.org import MatrixList
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
    0         FED RESERV BANK PHILA [USA] 005:01156    Jagtiani J. 005:01156    5
    1    SOUTHWEST UNIV FINANC ECON [CHN] 008:02269          Li X. 003:00894    5
    2                UNIV HONG KONG [HKG] 004:00760     Arner D.W. 003:00911    4
    3                UNIV HONG KONG [HKG] 004:00760    Barberis J. 003:00445    4
    4  MAX PLANCK INST INNOV COMPET [DEU] 003:00904      Hornuf L. 003:00904    3
    5                      UNIV ZÜR [CHE] 007:00971      Dolata M. 003:00330    3
    6                      UNIV ZÜR [CHE] 007:00971     Schwabe G. 003:00330    3
    7                      UNIV ZÜR [CHE] 007:00971  Zavolokina L. 003:00330    3
    8          ADA CHAIR FINANC LAW [LUX] 002:01062     Arner D.W. 003:00911    2
    9                   CESIFO GMBH [DEU] 002:00748      Hornuf L. 003:00904    2


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
