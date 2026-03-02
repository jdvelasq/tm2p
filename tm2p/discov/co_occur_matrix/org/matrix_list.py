"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.co_occur_matrix.org import MatrixList
    >>> df = (
    ...     MatrixList()
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
                                               rows  ... OCC
    0    SOUTHWEST UNIV FINANC ECON [CHN] 008:02269  ...  16
    1                      UNIV ZÜR [CHE] 007:00971  ...   9
    2                UNIV HONG KONG [HKG] 004:00760  ...   8
    3         FED RESERV BANK PHILA [USA] 005:01156  ...   5
    4                     LATV UNIV [LVA] 004:00456  ...   4
    5                   PEKING UNIV [CHN] 004:00576  ...   4
    6                               [N/A] 004:00192  ...   4
    7  MAX PLANCK INST INNOV COMPET [DEU] 003:00904  ...   3
    8                 SHANGHAI UNIV [CHN] 003:00911  ...   3
    9           XI'AN JIAOTONG UNIV [CHN] 003:00689  ...   3
    <BLANKLINE>
    [10 rows x 3 columns]


"""

from tm2p._intern import ParamsMixin

from ...occur_matrix._intern.matrix_list import MatrixList as BaseMatrixList
from ._field import SOURCE_FIELD


class MatrixList(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return (
            BaseMatrixList()
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
