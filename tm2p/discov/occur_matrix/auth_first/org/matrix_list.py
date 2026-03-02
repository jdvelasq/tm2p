"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.auth_first.org import MatrixList
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
    0           FED RESERV BANK PHILA [USA] 005:01156    Jagtiani J. 003:00682    3
    1                        UNIV ZÜR [CHE] 007:00971  Zavolokina L. 003:00330    3
    2            ADA CHAIR FINANC LAW [LUX] 002:01062     Arner D.W. 002:00898    2
    3                       DURH UNIV [GBR] 002:00474       Allen F. 002:00474    2
    4            FED RESERV BANK CHIC [USA] 002:00560    Jagtiani J. 003:00682    2
    5           FED RESERV BANK PHILA [USA] 005:01156       Allen F. 002:00474    2
    6       GOETHE-UNIVERSITÄT FRANKF [DEU] 002:02579      Gomber P. 002:02579    2
    7                   IMP COLL LOND [GBR] 002:00474       Allen F. 002:00474    2
    8                    JIANGSU UNIV [CHN] 002:00656     Muganyi T. 002:00656    2
    9  MAULANA AZAD NATL INST TECHNOL [IND] 002:00256    Nenavath S. 002:00256    2


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
