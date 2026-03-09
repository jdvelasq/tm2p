"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.tfidf import Matrix
    >>> df = (
    ...     Matrix()
    ...     #
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
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
    >>> df.head()
    AUTHKW_NORM                                         fintech 117:25478  ...  financial services 007:01673
    RID                                                                    ...
    Agarwal, 2020, ASIAPACIFIC J FINANC STUD, V49, ...                  1  ...                             0
    Ajouz, 2023, CUAD ECON, V46, P189                                   1  ...                             0
    Al-Sartawi, 2024, J FINANC REPORT ACCOUNT                           1  ...                             0
    Aldboush, 2023, INT J FINANC STUD, V11                              1  ...                             0
    Allen, 2021, REV CORP FINANC, V1, P259                              1  ...                             0
    <BLANKLINE>
    [5 rows x 10 columns]

    >>> df = (
    ...     Matrix()
    ...     #
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_tfidf_norm(None)
    ...     .using_tfidf_smooth_idf(False)
    ...     .using_tfidf_sublinear_tf(False)
    ...     .using_tfidf_use_idf(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()


"""

import pandas as pd  # type: ignore
from sklearn.feature_extraction.text import TfidfTransformer  # type: ignore

from tm2p._intern import ParamsMixin, SortAxesMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits
from tm2p.anal.metrics import Metrics
from tm2p.enum.column import COUNTERS, GCS, OCC, RID


class Matrix(
    ParamsMixin,
    SortAxesMixin,
):
    """:meta private:"""

    def _explode_dataframe(self, df, field):

        df = df.reset_index()
        df = df[
            [
                field,
                RID,
                GCS,
            ]
        ].copy()
        df = df.dropna()
        df[OCC] = 1
        df[field] = df[field].str.split(";")
        df = df.explode(field)
        df[field] = df[field].str.strip()

        return df

    def _get_items_mapping(self, df, field):

        df = df[[field, GCS, OCC]].copy()
        df = df.groupby(field).agg({OCC: "sum", GCS: "sum"})

        occ_digits, gcs_digits = get_zero_digits(self.params.root_directory)

        df[COUNTERS] = df.index.astype(str)
        df[COUNTERS] += " " + df[OCC].map(lambda x: f"{x:0{occ_digits}d}")
        df[COUNTERS] += ":" + df[GCS].map(lambda x: f"{x:0{gcs_digits}d}")

        mapping = df[COUNTERS].to_dict()

        return mapping

    def _create_matrix(self, df, field):

        df = df[[field, RID, OCC]].copy()
        df = df.dropna()

        grouped = df.groupby([RID, field], as_index=False).agg({OCC: "sum"})

        matrix = pd.pivot(
            index=RID,
            data=grouped,
            columns=field,
            values="OCC",
        )
        matrix = matrix.fillna(0)

        if self.params.binary_item_frequencies is True:
            matrix = matrix.map(lambda w: 1 if w > 0 else 0)

        return matrix

    def _filter_items_in_matrix(self, matrix):

        selected_items = (
            Metrics()
            .update(**self.params.__dict__)
            .with_source_field(self.params.source_field)
            .run()
        ).index.tolist()
        matrix = matrix[selected_items]
        return matrix

    def _remove_rows_of_zeros(self, matrix):
        matrix = matrix.loc[(matrix != 0).any(axis=1)]
        return matrix

    def _apply_tfidf_transformations(self, matrix):

        norm = self.params.tfidf_norm
        smooth_idf = self.params.tfidf_smooth_idf
        sublinear_tf = self.params.tfidf_sublinear_tf
        use_idf = self.params.tfidf_use_idf

        if norm is not None or use_idf or smooth_idf or sublinear_tf:

            transformer = TfidfTransformer(
                norm=norm,  # type: ignore
                use_idf=use_idf,
                smooth_idf=smooth_idf,
                sublinear_tf=sublinear_tf,
            )
            matrix = transformer.fit_transform(matrix)
        else:
            matrix = matrix.astype(int)

        return matrix

    def _append_counters_to_axis(self, data_frame, mapping):
        data_frame.columns = data_frame.columns.map(mapping)
        return data_frame

    def _sort_column(self, data_frame):
        return self.sort_columns(data_frame)

    def _remove_counters_from_axes(self, data_frame):
        if self.params.counters is False:
            data_frame.columns = [" ".join(x.split()[:-1]) for x in data_frame.columns]
        return data_frame

    def run(self):

        field = self.params.source_field.value

        df = load_filtered_main_csv_zip(params=self.params)
        df = self._explode_dataframe(df, field)

        mapping = self._get_items_mapping(df, field)

        matrix = self._create_matrix(df, field)
        matrix = self._filter_items_in_matrix(matrix)
        matrix = self._remove_rows_of_zeros(matrix)
        matrix = self._apply_tfidf_transformations(matrix)
        matrix = self._append_counters_to_axis(matrix, mapping)
        matrix = self._sort_column(matrix)
        matrix = self._remove_counters_from_axes(matrix)

        return matrix
