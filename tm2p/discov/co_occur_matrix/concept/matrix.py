"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.co_occur_matrix.concept import Matrix
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
    columns                         fintech 155:33245  ...  banking 025:04664
    rows                                               ...
    fintech 155:33245                             155  ...                 21
    financial technology 051:09258                 48  ...                  5
    finance 050:10972                              39  ...                  2
    innovation 033:07734                           30  ...                  4
    china 033:06419                                28  ...                  4
    financial services 030:06887                   28  ...                  8
    banks 029:06252                                25  ...                  9
    technology 028:05172                           25  ...                  2
    the development 026:05689                      22  ...                  5
    banking 025:04664                              21  ...                 25
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
