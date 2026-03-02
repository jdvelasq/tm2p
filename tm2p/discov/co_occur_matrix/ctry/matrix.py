"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.co_occur_matrix.ctry import Matrix
    >>> df = (
    ...     Matrix()
    ...     #
    ...     # FIELD:
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
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
    columns        CHN 045:09715  GBR 033:06802  ...  CHE 008:01458  ITA 008:01041
    rows                                         ...
    CHN 045:09715             45              3  ...              0              1
    GBR 033:06802              3             33  ...              1              2
    USA 031:09562              6              2  ...              0              1
    AUS 014:03468              2              3  ...              0              0
    DEU 013:05295              0              2  ...              0              2
    IND 012:01818              0              2  ...              0              0
    FRA 011:02475              2              2  ...              0              0
    KOR 011:02378              1              0  ...              0              0
    CHE 008:01458              0              1  ...              8              0
    ITA 008:01041              1              2  ...              0              8
    <BLANKLINE>
    [10 rows x 10 columns]




"""

from tm2p._intern import ParamsMixin

from ...occur_matrix._intern.matrix_list import Matrix as BaseMatrix
from ._field import SOURCE_FIELD


class Matrix(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            BaseMatrix()
            .update(**self.params.__dict__)
            #
            # COLUMNS:
            .with_column_field(SOURCE_FIELD)
            .having_column_items_in_top(self.params.top_n)
            .having_column_items_ordered_by(self.params.items_order_by)
            .having_column_item_occurrences_between(
                self.params.item_occurrences_range[0],
                self.params.item_occurrences_range[1],
            )
            .having_column_item_citations_between(
                self.params.item_citations_range[0],
                self.params.item_citations_range[1],
            )
            .having_column_items_in(self.params.items_in)
            #
            # ROWS:
            .with_index_field(SOURCE_FIELD)
            .having_index_items_in_top(self.params.top_n)
            .having_index_items_ordered_by(self.params.items_order_by)
            .having_index_item_occurrences_between(
                self.params.item_occurrences_range[0],
                self.params.item_occurrences_range[1],
            )
            .having_index_item_citations_between(
                self.params.item_citations_range[0],
                self.params.item_citations_range[1],
            )
            .having_index_items_in(self.params.items_in)
            #
            .run()
        )
