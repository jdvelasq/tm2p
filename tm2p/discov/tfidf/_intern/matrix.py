"""
Matrix
===============================================================================

Smoke tests:
    >>> from tm2p import CorpusField, ItemsOrderBy
    >>> from tm2p.discov.tfidf._intern import Matrix
    >>> df = (
    ...     Matrix()
    ...     #
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_item_counters(True)
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



"""

import pandas as pd  # type: ignore
from sklearn.feature_extraction.text import TfidfTransformer  # type: ignore

from tm2p import CorpusField
from tm2p._intern import ParamsMixin, SortAxesMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.get_zero_digits import get_zero_digits
from tm2p.anal._intern.performance.performance_metrics import (
    PerformanceMetrics as TermsByYearMetricsDataFrame,
)
from tm2p.ingest.extr import TopTermsExtractor

from ._field import SOURCE_FIELD

FIELD = SOURCE_FIELD.value
GLS = CorpusField.GCS.value
OCC = "OCC"
RID = CorpusField.RID.value


class Matrix(
    ParamsMixin,
    SortAxesMixin,
):
    """:meta private:"""

    def _step_1_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    def step_2_explode_data_frame(self, data_frame):

        data_frame = data_frame.reset_index()
        data_frame = data_frame[
            [
                FIELD,
                RID,
                GLS,
            ]
        ].copy()
        data_frame = data_frame.dropna()
        data_frame[OCC] = 1
        data_frame[FIELD] = data_frame[FIELD].str.split(";")
        data_frame = data_frame.explode(FIELD)
        data_frame[FIELD] = data_frame[FIELD].str.strip()

        return data_frame

    def step_3_get_terms_mapping(self, data_frame):

        data_frame = data_frame[[FIELD, GLS, OCC]].copy()
        data_frame = data_frame.groupby(FIELD).agg({OCC: "sum", GLS: "sum"})

        data_frame["counters"] = data_frame.index.astype(str)

        occ_digits, gcs_digits = get_zero_digits(self.params.root_directory)

        data_frame["counters"] += " " + data_frame[OCC].map(
            lambda x: f"{x:0{occ_digits}d}"
        )

        data_frame["counters"] += ":" + data_frame[GLS].map(
            lambda x: f"{x:0{gcs_digits}d}"
        )

        mapping = data_frame["counters"].to_dict()

        return mapping

    def step_4_create_df_matrix(self, data_frame):

        data_frame = data_frame[[FIELD, RID, OCC]].copy()
        data_frame = data_frame.dropna()

        grouped = data_frame.groupby([RID, FIELD], as_index=False).agg({OCC: "sum"})

        matrix = pd.pivot(
            index=RID,
            data=grouped,
            columns=FIELD,
            values="OCC",
        )
        matrix = matrix.fillna(0)

        if self.params.binary_item_frequencies is True:
            matrix = matrix.map(lambda w: 1 if w > 0 else 0)

        return matrix

    def step_5_filter_terms_in_df_matrix(self, matrix):

        selected_items = TopTermsExtractor().update(**self.params.__dict__).run()
        matrix = matrix[selected_items]
        return matrix

    def step_6_remove_rows_of_zeros(self, df_matrix):
        df_matrix = df_matrix.loc[(df_matrix != 0).any(axis=1)]
        return df_matrix

    def step_7_apply_tfidf_transformations(self, matrix):

        norm = self.params.tfidf_norm
        smooth_idf = self.params.tfidf_smooth_idf
        sublinear_tf = self.params.tfidf_sublinear_tf
        use_idf = self.params.tfidf_use_idf

        if norm is not None or use_idf or smooth_idf or sublinear_tf:

            transformer = TfidfTransformer(
                norm=norm,
                use_idf=use_idf,
                smooth_idf=smooth_idf,
                sublinear_tf=sublinear_tf,
            )
            matrix = transformer.fit_transform(matrix)
        else:
            matrix = matrix.astype(int)

        return matrix

    def step_8_append_counters_to_axis(self, data_frame, mapping):
        data_frame.columns = data_frame.columns.map(mapping)
        return data_frame

    def step_9_sort_columns(self, data_frame):
        return self.sort_columns(data_frame)

    def step_10_remove_counters_from_axes(self, data_frame):
        if self.params.item_counters is False:
            data_frame.columns = [" ".join(x.split()[:-1]) for x in data_frame.columns]
        return data_frame

    def run(self):

        df = self._step_1_load_the_database()
        df = self.step_2_explode_data_frame(df)

        mapping = self.step_3_get_terms_mapping(df)

        matrix = self.step_4_create_df_matrix(df)
        matrix = self.step_5_filter_terms_in_df_matrix(matrix)
        matrix = self.step_6_remove_rows_of_zeros(matrix)
        matrix = self.step_7_apply_tfidf_transformations(matrix)
        matrix = self.step_8_append_counters_to_axis(matrix, mapping)
        matrix = self.step_9_sort_columns(matrix)
        matrix = self.step_10_remove_counters_from_axes(matrix)

        return matrix
