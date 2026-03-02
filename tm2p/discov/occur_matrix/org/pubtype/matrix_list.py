"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemsOrderBy
    >>> from tm2p.discov.occur_matrix.org.pubtype import MatrixList
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
                    rows                                       columns  OCC
    0  Article 142:32733    SOUTHWEST UNIV FINANC ECON [CHN] 008:02269    8
    1  Article 142:32733                   PEKING UNIV [CHN] 004:00576    4
    2  Article 142:32733                UNIV HONG KONG [HKG] 004:00760    4
    3  Article 142:32733                      UNIV ZÜR [CHE] 007:00971    4
    4  Article 142:32733         FED RESERV BANK PHILA [USA] 005:01156    3
    5  Article 142:32733                     LATV UNIV [LVA] 004:00456    3
    6  Article 142:32733                 SHANGHAI UNIV [CHN] 003:00911    3
    7  Article 142:32733           XI'AN JIAOTONG UNIV [CHN] 003:00689    3
    8  Article 142:32733  MAX PLANCK INST INNOV COMPET [DEU] 003:00904    2
    9  Article 142:32733                               [N/A] 004:00192    2


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
