"""
Smoke tests:
    >>> from tm2p import CorpusField, ItemsOrderBy
    >>> from tm2p import CorpusField
    >>> from tm2p.analyze._intern.performance import PerformanceMetrics
    >>> df = (
    ...     PerformanceMetrics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(CorpusField.AUTH_KEY_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemsOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df # doctest: +SKIP
                             rank_occ  ...                           counters
    AUTH_KEY_NORM                      ...
    fintech                         1  ...                  fintech 117:25478
    financial inclusion             2  ...      financial inclusion 017:03823
    financial technology            3  ...     financial technology 014:02508
    green finance                   4  ...            green finance 011:02844
    blockchain                      5  ...               blockchain 011:02023
    banking                         6  ...                  banking 010:02599
    china                           7  ...                    china 009:01947
    innovation                      8  ...               innovation 009:01703
    artificial intelligence         9  ...  artificial intelligence 008:01915
    financial services             10  ...       financial services 007:01673
    <BLANKLINE>
    [10 rows x 17 columns]


"""

import pandas as pd  # type: ignore

from tm2p import CorpusField, ItemsOrderBy
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

SELECTED_COLUMNS = {
    ItemsOrderBy.OCC.value: [
        ItemsOrderBy.OCC.value,
        CorpusField.GCS.value,
        CorpusField.LCS.value,
        "_name_",
    ],
    #
    CorpusField.GCS.value: [
        CorpusField.GCS.value,
        CorpusField.LCS.value,
        ItemsOrderBy.OCC.value,
        "_name_",
    ],
    # -------------------------------------------
    CorpusField.LCS.value: [
        CorpusField.LCS.value,
        CorpusField.GCS.value,
        ItemsOrderBy.OCC.value,
        "_name_",
    ],
}


class PerformanceMetrics(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def step_01_load_filtered_main_data(self) -> pd.DataFrame:

        df = load_filtered_main_csv_zip(params=self.params)
        df = (
            df[
                [
                    self.params.source_field.value,
                    CorpusField.GCS.value,
                    CorpusField.LCS.value,
                    CorpusField.YEAR.value,
                ]
            ]
            .dropna()
            .copy()
        )

        return df

    # -------------------------------------------------------------------------
    def step_02_explode_source_field(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        source_field = self.params.source_field.value
        df[source_field] = df[source_field].str.split("; ")
        df = df.explode(source_field)

        return df

    # -------------------------------------------------------------------------
    def step_03_compute_primary_performance_metrics(self, df):

        source_field = self.params.source_field.value
        gcs = CorpusField.GCS.value
        lcs = CorpusField.LCS.value
        pubyear = CorpusField.YEAR.value

        df = df.sort_values(
            [
                source_field,
                gcs,
                lcs,
            ],
            ascending=[
                True,
                False,
                False,
            ],
        )

        df = df.assign(position=df.groupby(source_field).cumcount() + 1)
        df = df.assign(position2=df.position.map(lambda w: w * w))
        df = df.reset_index(drop=True)

        df["OCC"] = 1
        grouped_df = df.groupby(source_field).agg(
            {
                "OCC": "sum",
                gcs: "sum",
                lcs: "sum",
                pubyear: "min",
            }
        )
        grouped_df = grouped_df.rename(columns={pubyear: "first_publication_year"})
        grouped_df["last_year"] = df[pubyear].max()

        return df, grouped_df

    # -------------------------------------------------------------------------
    def step_04_compute_derived_performance_metrics(self, grouped_df):

        gcs = CorpusField.GCS.value
        lcs = CorpusField.LCS.value
        occ = ItemsOrderBy.OCC.value

        grouped_df = grouped_df.copy()
        grouped_df["age"] = (
            grouped_df["last_year"] - grouped_df["first_publication_year"] + 1
        )
        grouped_df["global_citations_per_year"] = grouped_df[gcs] / grouped_df["age"]
        grouped_df["local_citations_per_year"] = grouped_df[lcs] / grouped_df["age"]

        grouped_df["global_citations_per_document"] = grouped_df[gcs] / grouped_df[occ]
        grouped_df["local_citations_per_document"] = grouped_df[lcs] / grouped_df[occ]
        return grouped_df

    # -------------------------------------------------------------------------
    def step_05_compute_impact_metrics(self, df, grouped_df):

        source_field = self.params.source_field.value
        gcs = CorpusField.GCS.value
        # cit_count_local = CorpusField.CIT_COUNT_LOCAL.value

        df = df.copy()
        grouped_df = grouped_df.copy()

        # H-index
        h_indexes = df.query(f"{gcs} >= position")
        h_indexes = h_indexes.groupby(source_field, as_index=True).agg(
            {"position": "max"}
        )
        h_indexes = h_indexes.rename(columns={"position": "h_index"})
        grouped_df.loc[h_indexes.index, "h_index"] = h_indexes.astype(int)
        grouped_df["h_index"] = grouped_df["h_index"].fillna(0)

        # G-index
        g_indexes = df.query(f"{gcs} >= position2")
        g_indexes = g_indexes.groupby(source_field, as_index=True).agg(
            {"position": "max"}
        )
        g_indexes = g_indexes.rename(columns={"position": "g_index"})
        grouped_df.loc[g_indexes.index, "g_index"] = g_indexes.astype(int)
        grouped_df["g_index"] = grouped_df["g_index"].fillna(0)

        # M-index
        grouped_df = grouped_df.assign(m_index=grouped_df.h_index / grouped_df.age)
        grouped_df["m_index"] = grouped_df.m_index.round(decimals=2)

        return grouped_df

    # -------------------------------------------------------------------------
    def sort_data_frame_by_metric(self, df, metric):

        df = df.copy()
        df["_name_"] = df.index.tolist()

        columns = SELECTED_COLUMNS[metric]
        ascending = [False] * (len(columns) - 1) + [True]

        df = df.sort_values(columns, ascending=ascending)
        df = df.drop(columns=["_name_"])

        return df

    # -------------------------------------------------------------------------
    def step_06_add_rank_columns(self, grouped_df):

        cit_count_global = CorpusField.GCS.value
        cit_count_local = CorpusField.LCS.value
        occ = ItemsOrderBy.OCC.value

        grouped_df = grouped_df.copy()

        grouped_df = self.sort_data_frame_by_metric(grouped_df, cit_count_local)
        grouped_df.insert(0, "rank_lcs", range(1, len(grouped_df) + 1))

        grouped_df = self.sort_data_frame_by_metric(grouped_df, cit_count_global)
        grouped_df.insert(0, "rank_gcs", range(1, len(grouped_df) + 1))

        grouped_df = self.sort_data_frame_by_metric(grouped_df, occ)
        grouped_df.insert(0, "rank_occ", range(1, len(grouped_df) + 1))

        return grouped_df

    # -------------------------------------------------------------------------
    def step_07_filter_by_term_occurrences_range(self, grouped_df):

        occ = ItemsOrderBy.OCC.value

        grouped_df = grouped_df.copy()

        if self.params.item_occurrences_range is None:
            return grouped_df

        min_value, max_value = self.params.item_occurrences_range

        if min_value is not None:
            grouped_df = grouped_df[grouped_df[occ] >= min_value]
        if max_value is not None:
            grouped_df = grouped_df[grouped_df[occ] <= max_value]

        return grouped_df

    # -------------------------------------------------------------------------
    def step_08_filter_by_term_citations_range(self, grouped_df):

        cit_count_global = CorpusField.GCS.value
        # cit_count_local = CorpusField.CIT_COUNT_LOCAL.value

        grouped_df = grouped_df.copy()

        if self.params.item_citations_range is None:
            return grouped_df

        min_value, max_value = self.params.item_citations_range

        if min_value is not None:
            grouped_df = grouped_df[grouped_df[cit_count_global] >= min_value]
        if max_value is not None:
            grouped_df = grouped_df[grouped_df[cit_count_global] <= max_value]

        return grouped_df

    # -------------------------------------------------------------------------
    def step_09_filter_by_terms_in(self, grouped_df):

        grouped_df = grouped_df.copy()

        if self.params.items_in is None:
            return grouped_df

        if self.params.items_in is not None:
            #
            terms_in = [t for t in self.params.items_in if t in grouped_df.index]
            #
            grouped_df = grouped_df.loc[terms_in, :]

        return grouped_df

    # -------------------------------------------------------------------------
    def step_10_filter_by_top_n_terms(self, grouped_df):

        grouped_df = self.sort_data_frame_by_metric(
            df=grouped_df.copy(),
            metric=self.params.items_order_by.value,
        )

        if self.params.top_n is not None:
            grouped_df = grouped_df.head(self.params.top_n)

        return grouped_df

    # -------------------------------------------------------------------------
    def step_11_check_field_types(self, grouped_df):

        grouped_df = grouped_df.copy()

        if "OCC" in grouped_df.columns:
            grouped_df["OCC"] = grouped_df["OCC"].astype(int)

        if CorpusField.GCS.value in grouped_df.columns:
            grouped_df[CorpusField.GCS.value] = grouped_df[
                CorpusField.GCS.value
            ].astype(int)

        if CorpusField.LCS.value in grouped_df.columns:
            grouped_df[CorpusField.LCS.value] = grouped_df[
                CorpusField.LCS.value
            ].astype(int)

        if "h_index" in grouped_df.columns:
            grouped_df["h_index"] = grouped_df["h_index"].astype(int)

        if "g_index" in grouped_df.columns:
            grouped_df["g_index"] = grouped_df["g_index"].astype(int)

        return grouped_df

    # -------------------------------------------------------------------------
    def step_12_add_term_with_counters_column(self, grouped_df):

        from tm2p._intern.get_zero_digits import get_zero_digits

        gcs = CorpusField.GCS.value
        occ = ItemsOrderBy.OCC.value

        occ_zeros, gcs_zeros = get_zero_digits(
            root_directory=self.params.root_directory
        )

        grouped_df = grouped_df.copy()
        grouped_df["counters"] = grouped_df.index.astype(str)

        grouped_df["counters"] += " " + grouped_df[occ].map(
            lambda x: f"{x:0{occ_zeros}d}"
        )

        grouped_df["counters"] += ":" + grouped_df[gcs].map(
            lambda x: f"{x:0{gcs_zeros}d}"
        )

        return grouped_df

    # -------------------------------------------------------------------------
    def run(self):

        df = self.step_01_load_filtered_main_data()
        df = self.step_02_explode_source_field(df)
        df, grouped_df = self.step_03_compute_primary_performance_metrics(df)
        grouped_df = self.step_04_compute_derived_performance_metrics(grouped_df)
        grouped_df = self.step_05_compute_impact_metrics(df, grouped_df)
        grouped_df = self.step_06_add_rank_columns(grouped_df)
        grouped_df = self.step_07_filter_by_term_occurrences_range(grouped_df)
        grouped_df = self.step_08_filter_by_term_citations_range(grouped_df)
        grouped_df = self.step_09_filter_by_terms_in(grouped_df)
        grouped_df = self.step_10_filter_by_top_n_terms(grouped_df)
        grouped_df = self.step_11_check_field_types(grouped_df)
        grouped_df = self.step_12_add_term_with_counters_column(grouped_df)

        return grouped_df


#
