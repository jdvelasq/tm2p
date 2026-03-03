"""
MatrixList
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import MatrixList
    >>> df = (
    ...     MatrixList()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(Field.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(Field.AUTH_NORM)
    ...     .having_index_items_in_top(None)
    ...     .having_index_items_ordered_by(ItemOrderBy.OCC)
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
                          rows            columns  OCC
    0    Jagtiani J. 005:01156  fintech 117:25478    5
    1      Dolata M. 003:00330  fintech 117:25478    3
    2      Hornuf L. 003:00904  fintech 117:25478    3
    3          Li X. 003:00894  fintech 117:25478    3
    4     Schwabe G. 003:00330  fintech 117:25478    3
    5  Zavolokina L. 003:00330  fintech 117:25478    3
    6   Al-Okaily M. 002:00191  fintech 117:25478    2
    7  Al-Sartawi A. 002:00274  fintech 117:25478    2
    8       Allen F. 002:00474  fintech 117:25478    2
    9     Arner D.W. 003:00911  fintech 117:25478    2



    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import MatrixList
    >>> df = (
    ...     MatrixList()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(Field.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(Field.AUTH_NORM)
    ...     .having_index_items_in_top(10)
    ...     .having_index_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_index_item_occurrences_between(None, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(False)
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
                          rows               columns  OCC
    0    Jagtiani J. 005:01156     fintech 117:25478    5
    1      Dolata M. 003:00330     fintech 117:25478    3
    2      Hornuf L. 003:00904     fintech 117:25478    3
    3          Li X. 003:00894     fintech 117:25478    3
    4     Schwabe G. 003:00330     fintech 117:25478    3
    5  Zavolokina L. 003:00330     fintech 117:25478    3
    6     Arner D.W. 003:00911     fintech 117:25478    2
    7      Dolata M. 003:00330  innovation 009:01703    2
    8     Schwabe G. 003:00330  innovation 009:01703    2
    9  Zavolokina L. 003:00330  innovation 009:01703    2


"""

from tm2p._intern import ParamsMixin

from .matrix import Matrix


class MatrixList(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_compute_co_occurence_matrix(self):
        return (
            Matrix()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .using_item_counters(True)
            .run()
        )

    # -------------------------------------------------------------------------
    def _step_02_melt_matrix(self, matrix):
        matrix = matrix.reset_index(drop=False)
        matrix_list = matrix.melt(
            id_vars=["rows"],
            value_vars=matrix.columns,
            var_name="columns",
        )
        matrix_list = matrix_list.rename(columns={"value": "OCC"})
        matrix_list = matrix_list.sort_values(
            by=["OCC", "rows", "columns"],
            ascending=[False, True, True],
        )
        matrix_list = matrix_list.reset_index(drop=True)
        return matrix_list

    # -------------------------------------------------------------------------
    def run(self):

        matrix = self._step_01_compute_co_occurence_matrix()
        matrix_list = self._step_02_melt_matrix(matrix)

        return matrix_list
