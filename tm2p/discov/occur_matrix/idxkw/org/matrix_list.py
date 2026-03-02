"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.idxkw.org import MatrixList
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
                                           rows  ... OCC
    0           HORIZ UNIV COLL [ARE] 003:00254  ...   4
    1  TASHKENT STATE UNIV ECON [UZB] 003:00254  ...   4
    2     AL-AHLIYYA AMMAN UNIV [JOR] 002:00170  ...   3
    3         APPL SCI RES CENT [JOR] 002:00170  ...   3
    4         BEIJING NORM UNIV [CHN] 002:00270  ...   2
    5             EXCEL BUS SCH [FRA] 002:00280  ...   2
    6             EXCEL BUS SCH [FRA] 002:00280  ...   2
    7             EXCEL BUS SCH [FRA] 002:00280  ...   2
    8                FUDAN UNIV [CHN] 002:00670  ...   2
    9                FUDAN UNIV [CHN] 002:00670  ...   2
    <BLANKLINE>
    [10 rows x 3 columns]


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
