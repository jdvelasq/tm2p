"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.auth.auth_first import MatrixList
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
    0    Jagtiani J. 003:00682    Jagtiani J. 005:01156    3
    1  Zavolokina L. 003:00330      Dolata M. 003:00330    3
    2  Zavolokina L. 003:00330     Schwabe G. 003:00330    3
    3  Zavolokina L. 003:00330  Zavolokina L. 003:00330    3
    4       Allen F. 002:00474    Jagtiani J. 005:01156    2
    5     Arner D.W. 002:00898     Arner D.W. 003:00911    2
    6      Gomber P. 002:02579      Gomber P. 002:02579    2
    7     Arner D.W. 002:00898    Barberis J. 003:00445    1
    8     Chishti S. 002:00096    Barberis J. 003:00445    1
    9      Gomber P. 002:02579  Kauffman R.J. 002:01445    1


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
