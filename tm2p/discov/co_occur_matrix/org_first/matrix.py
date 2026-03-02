"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.co_occur_matrix.org_first import Matrix
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
    columns                                     SOUTHWEST UNIV FINANC ECON [CHN] 005:01236  ...  IMP COLL LOND [GBR] 002:00474
    rows                                                                                    ...
    SOUTHWEST UNIV FINANC ECON [CHN] 005:01236                                           5  ...                              0
    UNIV ZÜR [CHE] 005:00659                                                             0  ...                              0
    [N/A] 004:00192                                                                      0  ...                              0
    XI'AN JIAOTONG UNIV [CHN] 003:00689                                                  0  ...                              0
    FED RESERV BANK PHILA [USA] 003:00682                                                0  ...                              0
    GOETHE-UNIVERSITÄT FRANKF [DEU] 002:02579                                            0  ...                              0
    SOAS UNIV LOND [GBR] 002:01022                                                       0  ...                              0
    SHANGHAI UNIV [CHN] 002:00656                                                        0  ...                              0
    PACE UNIV [USA] 002:00511                                                            0  ...                              0
    IMP COLL LOND [GBR] 002:00474                                                        0  ...                              2
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
