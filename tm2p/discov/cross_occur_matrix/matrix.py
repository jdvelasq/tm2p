"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import Matrix
    >>> df = (
    ...     Matrix()
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
    >>> df.head(10)  # doctest: +SKIP
    columns                  fintech 117:25478  ...  financial services 007:01673
    rows                                        ...
    Jagtiani J. 005:01156                    5  ...                             0
    Arner D.W. 003:00911                     2  ...                             0
    Hornuf L. 003:00904                      3  ...                             0
    Li X. 003:00894                          3  ...                             0
    Barberis J. 003:00445                    1  ...                             0
    Dolata M. 003:00330                      3  ...                             0
    Schwabe G. 003:00330                     3  ...                             0
    Zavolokina L. 003:00330                  3  ...                             0
    Gomber P. 002:02579                      1  ...                             0
    Kauffman R.J. 002:01445                  0  ...                             0
    <BLANKLINE>
    [10 rows x 10 columns]


    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import Matrix
    >>> df = (
    ...     Matrix()
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
    ...     .where_records_match(
    ...         {
    ...             Field.AUTHKW_RAW: ["fintech", "innovation", "financial services"],
    ...         },
    ...     )
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 1
    True
    >>> df.shape[1] > 1
    True
    >>> df.head(10)  # doctest: +SKIP
                      fintech  financial inclusion  ...  banking  financial markets
    Brooks S.               1                    1  ...        0                  0
    Gabor D.                1                    1  ...        0                  0
    Ashta A.                1                    0  ...        1                  1
    Herrmann H.             1                    0  ...        1                  1
    Jagtiani J.             1                    0  ...        0                  0
    Lemieux C.              1                    0  ...        0                  0
    Muchapondwa E.          1                    0  ...        0                  0
    Udeagha M.C.            1                    0  ...        0                  0
    Lagna A.                1                    1  ...        0                  0
    Ravishankar M.N.        1                    1  ...        0                  0
    <BLANKLINE>
    [10 rows x 10 columns]



"""

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.anal.metrics import Metrics


class Matrix(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_01_compute_column_peformance_metrics(self):
        metrics = (
            Metrics()
            .update(**self.params.__dict__)
            .with_source_field(self.params.column_field)
            .having_items_in_top(self.params.column_top_n)
            .having_items_ordered_by(self.params.column_items_order_by)
            .having_item_occurrences_between(
                self.params.column_item_occurrences_range[0],
                self.params.column_item_occurrences_range[1],
            )
            .having_item_citations_between(
                self.params.column_item_citations_range[0],
                self.params.column_item_citations_range[1],
            )
            .having_items_in(self.params.column_items_in)
            .run()
        )
        return metrics

    # -------------------------------------------------------------------------
    def _step_02_compute_row_peformance_metrics(self):
        metrics = (
            Metrics()
            .update(**self.params.__dict__)
            .with_source_field(self.params.index_field)
            .having_items_in_top(self.params.index_top_n)
            .having_items_ordered_by(self.params.index_items_order_by)
            .having_item_occurrences_between(
                self.params.index_item_occurrences_range[0],
                self.params.index_item_occurrences_range[1],
            )
            .having_item_citations_between(
                self.params.index_item_citations_range[0],
                self.params.index_item_citations_range[1],
            )
            .having_items_in(self.params.index_items_in)
            .run()
        )
        return metrics

    # -------------------------------------------------------------------------
    def _step_03_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def _step_04_create_raw_matrix_list(self, records):
        #
        columns = self.params.column_field.value
        rows = self.params.index_field.value
        #
        raw_matrix_list = records[[columns]].copy()
        raw_matrix_list = raw_matrix_list.rename(columns={columns: "columns"})
        raw_matrix_list = raw_matrix_list.assign(rows=records[[rows]])
        #
        return raw_matrix_list

    # -------------------------------------------------------------------------
    def _step_05_explode_matrix_list(self, raw_matrix_list, name, selected_terms):
        #
        raw_matrix_list[name] = raw_matrix_list[name].str.split(";")
        raw_matrix_list = raw_matrix_list.explode(name)
        raw_matrix_list[name] = raw_matrix_list[name].str.strip()
        raw_matrix_list = raw_matrix_list[raw_matrix_list[name].isin(selected_terms)]
        #
        return raw_matrix_list

    # -------------------------------------------------------------------------
    def _step_06_compute_occurrences(self, raw_matrix_list):
        #
        raw_matrix_list["OCC"] = 1
        raw_matrix_list = raw_matrix_list.groupby(
            ["rows", "columns"], as_index=False
        ).aggregate("sum")
        #
        raw_matrix_list = raw_matrix_list.sort_values(
            ["OCC", "rows", "columns"], ascending=[False, True, True]
        )
        raw_matrix_list = raw_matrix_list.reset_index(drop=True)
        #
        return raw_matrix_list

    # -------------------------------------------------------------------------
    def _step_07_build_mapping(self, dataframe):

        from tm2p._intern.get_zero_digits import get_zero_digits

        GCS = Field.GCS.value

        dataframe["counters"] = dataframe.index.astype(str)

        occ_digits, gcs_digits = get_zero_digits(self.params.root_directory)

        dataframe["counters"] += " " + dataframe["OCC"].map(
            lambda x: f"{x:0{occ_digits}d}"
        )

        dataframe["counters"] += ":" + dataframe[GCS].map(
            lambda x: f"{x:0{gcs_digits}d}"
        )

        mapping = dataframe["counters"].to_dict()

        return mapping

    # -------------------------------------------------------------------------
    def _step_08_rename_terms(self, raw_matrix_list, row_mapping, column_mapping):
        #
        raw_matrix_list["rows"] = raw_matrix_list["rows"].map(row_mapping)
        raw_matrix_list["columns"] = raw_matrix_list["columns"].map(column_mapping)
        #
        return raw_matrix_list

    # -------------------------------------------------------------------------
    def _step_09_pivot_matrix_list(self, matrix_list):
        matrix = matrix_list.pivot(
            index=matrix_list.columns[0],
            columns=matrix_list.columns[1],
            values=matrix_list.columns[2],
        )
        matrix = matrix.fillna(0)
        matrix = matrix.astype(int)
        return matrix

    # -------------------------------------------------------------------------
    def _step_10_check_terms(self, matrix, row_mapping, col_mapping):

        for _, value in row_mapping.items():
            if value not in matrix.index:
                matrix.loc[value] = 0

        for _, value in col_mapping.items():
            if value not in matrix.columns:
                matrix[value] = 0

        return matrix

    # -------------------------------------------------------------------------
    def _step_11_sort_matrix_axis(self, matrix):
        matrix_cols = matrix.columns.tolist()
        matrix_rows = matrix.index.tolist()
        matrix_cols = sorted(matrix_cols, key=lambda x: x.split()[-1], reverse=True)
        matrix_rows = sorted(matrix_rows, key=lambda x: x.split()[-1], reverse=True)
        matrix = matrix[matrix_cols]
        matrix = matrix.loc[matrix_rows]
        return matrix

    # -------------------------------------------------------------------------
    def _step_12_remove_counters(self, matrix):
        if self.params.item_counters is False:
            matrix_cols = [" ".join(col.split()[:-1]) for col in matrix.columns]
            matrix_rows = [" ".join(row.split()[:-1]) for row in matrix.index]
            matrix.columns = matrix_cols
            matrix.index = matrix_rows
        return matrix

    # -------------------------------------------------------------------------
    def run(self):

        col_metrics = self._step_01_compute_column_peformance_metrics()
        row_metrics = self._step_02_compute_row_peformance_metrics()

        records = self._step_03_load_the_database()

        matrix_list = self._step_04_create_raw_matrix_list(records)
        matrix_list = self._step_05_explode_matrix_list(
            matrix_list,
            "columns",
            col_metrics.index.tolist(),
        )
        matrix_list = self._step_05_explode_matrix_list(
            matrix_list,
            "rows",
            row_metrics.index.tolist(),
        )

        matrix_list = self._step_06_compute_occurrences(matrix_list)

        row_mapping = self._step_07_build_mapping(row_metrics)
        col_mapping = self._step_07_build_mapping(col_metrics)

        matrix_list = self._step_08_rename_terms(matrix_list, row_mapping, col_mapping)

        matrix = self._step_09_pivot_matrix_list(matrix_list)
        matrix = self._step_10_check_terms(matrix, row_mapping, col_mapping)
        matrix = self._step_11_sort_matrix_axis(matrix)
        matrix = self._step_12_remove_counters(matrix)

        return matrix
