"""
Metrics
===============================================================================


Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p import Field
    >>> from tm2p.anal.metrics import Metrics
    >>> df = (
    ...     Metrics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 1
    True
    >>> df.shape[1] > 1
    True
    >>> print(df.head(10).to_string())  # doctest: +NORMALIZE_WHITESPACE
                             RANK_OCC  RANK_GCS  RANK_LCS  OCC    GCS  LCS  YEAR_FIRST  YEAR_LAST  AGE  GCS_PER_YEAR  LCS_PER_YEAR  GCS_PER_DOC  LCS_PER_DOC  H_INDEX  G_INDEX  M_INDEX                           COUNTERS
    AUTHKW_NORM
    fintech                         1         1         1  117  25478    0        2016       2024    9   2830.888889           0.0   217.760684          0.0       97       17    10.78                  fintech 117:25478
    financial inclusion             2         2         2   17   3823    0        2016       2024    9    424.777778           0.0   224.882353          0.0       17       11     1.89      financial inclusion 017:03823
    financial technology            3         5         5   14   2508    0        2016       2024    9    278.666667           0.0   179.142857          0.0       13       10     1.44     financial technology 014:02508
    green finance                   4         3         3   11   2844    0        2021       2024    4    711.000000           0.0   258.545455          0.0       11       10     2.75            green finance 011:02844
    blockchain                      5         7         7   11   2023    0        2016       2024    9    224.777778           0.0   183.909091          0.0       11        8     1.22               blockchain 011:02023
    banking                         6         4         4   10   2599    0        2016       2024    9    288.777778           0.0   259.900000          0.0       10        8     1.11                  banking 010:02599
    china                           7         8         8    9   1947    0        2016       2024    9    216.333333           0.0   216.333333          0.0        9        8     1.00                    china 009:01947
    innovation                      8        10        10    9   1703    0        2016       2024    9    189.222222           0.0   189.222222          0.0        9        9     1.00               innovation 009:01703
    artificial intelligence         9         9         9    8   1915    0        2019       2024    6    319.166667           0.0   239.375000          0.0        8        8     1.33  artificial intelligence 008:01915
    financial services             10        11        11    7   1673    0        2016       2024    9    185.888889           0.0   239.000000          0.0        7        7     0.78       financial services 007:01673

    >>> from pprint import pprint
    >>> pprint(df.columns.tolist())
    ['RANK_OCC',
     'RANK_GCS',
     'RANK_LCS',
     'OCC',
     'GCS',
     'LCS',
     'YEAR_FIRST',
     'YEAR_LAST',
     'AGE',
     'GCS_PER_YEAR',
     'LCS_PER_YEAR',
     'GCS_PER_DOC',
     'LCS_PER_DOC',
     'H_INDEX',
     'G_INDEX',
     'M_INDEX',
     'COUNTERS']


"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.enum.column import (
    AGE,
    COUNTERS,
    G_INDEX,
    GCS,
    GCS_PER_DOC,
    GCS_PER_YEAR,
    H_INDEX,
    LCS,
    LCS_PER_DOC,
    LCS_PER_YEAR,
    M_INDEX,
    OCC,
    RANK_GCS,
    RANK_LCS,
    RANK_OCC,
    YEAR,
    YEAR_FIRST,
    YEAR_LAST,
)

POS = "POS"
POS2 = "POS2"

SELECTED_COLUMNS = {
    OCC: [
        OCC,
        GCS,
        LCS,
        "_name_",
    ],
    #
    GCS: [
        GCS,
        LCS,
        OCC,
        "_name_",
    ],
    # -------------------------------------------
    LCS: [
        LCS,
        GCS,
        OCC,
        "_name_",
    ],
}


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _load_filtered_main_csv_zip(self) -> pd.DataFrame:

        df = load_filtered_main_csv_zip(params=self.params)
        df = df[
            [
                self.params.source_field.value,
                GCS,
                LCS,
                YEAR,
            ]
        ].dropna()

        return df  # type: ignore

    # -------------------------------------------------------------------------
    def _explode_source_field(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        source_field = self.params.source_field.value
        df[source_field] = df[source_field].str.split("; ")
        df = df.explode(source_field)

        return df

    # -------------------------------------------------------------------------
    def _filter_stopitems(self, df):

        df = df.copy()
        source_field = self.params.source_field.value
        df = df[~df[source_field].str.startswith("#")]

        return df

    # -------------------------------------------------------------------------
    def _compute_primary_bibliometric_indicators(self, df):

        source_field = self.params.source_field.value

        df = df.sort_values(
            [
                source_field,
                GCS,
                LCS,
            ],
            ascending=[True, False, False],
        )

        df[POS] = df.groupby(source_field).cumcount() + 1
        df[POS2] = df[POS].map(lambda w: w * w)
        df = df.reset_index(drop=True)

        df["OCC"] = 1
        grouped_df = df.groupby(source_field).agg(
            {
                OCC: "sum",
                GCS: "sum",
                LCS: "sum",
                YEAR: "min",
            }
        )
        grouped_df = grouped_df.rename(columns={YEAR: YEAR_FIRST})
        grouped_df[YEAR_LAST] = df[YEAR].max()

        return df, grouped_df

    # -------------------------------------------------------------------------
    def _compute_derived_bibliometric_indicators(self, grouped_df):

        grouped_df = grouped_df.copy()

        grouped_df[AGE] = grouped_df[YEAR_LAST] - grouped_df[YEAR_FIRST] + 1

        grouped_df[GCS_PER_YEAR] = grouped_df[GCS] / grouped_df[AGE]
        grouped_df[LCS_PER_YEAR] = grouped_df[LCS] / grouped_df[AGE]

        grouped_df[GCS_PER_DOC] = grouped_df[GCS] / grouped_df[OCC]
        grouped_df[LCS_PER_DOC] = grouped_df[LCS] / grouped_df[OCC]

        return grouped_df

    # -------------------------------------------------------------------------
    def _compute_h_index(self, df, grouped_df):

        source_field = self.params.source_field.value

        df = df.copy()
        grouped_df = grouped_df.copy()

        h_indexes = df.query(f"{GCS} >= {POS}")
        h_indexes = h_indexes.groupby(source_field, as_index=True).agg(
            {f"{POS}": "max"}
        )
        h_indexes = h_indexes.rename(columns={f"{POS}": H_INDEX})
        grouped_df.loc[h_indexes.index, H_INDEX] = h_indexes.astype(int)
        grouped_df[H_INDEX] = grouped_df[H_INDEX].fillna(0)

        return grouped_df

    # -------------------------------------------------------------------------
    def _compute_g_index(self, df, grouped_df):

        source_field = self.params.source_field.value

        df = df.copy()
        grouped_df = grouped_df.copy()

        g_indexes = df.query(f"{GCS} >= {POS2}")
        g_indexes = g_indexes.groupby(source_field, as_index=True).agg({POS: "max"})
        g_indexes = g_indexes.rename(columns={POS: G_INDEX})
        grouped_df.loc[g_indexes.index, G_INDEX] = g_indexes.astype(int)
        grouped_df[G_INDEX] = grouped_df[G_INDEX].fillna(0)

        return grouped_df

    # -------------------------------------------------------------------------
    def _compute_m_index(self, df, grouped_df):

        df = df.copy()
        grouped_df = grouped_df.copy()

        grouped_df[M_INDEX] = grouped_df[H_INDEX] / grouped_df[AGE]
        grouped_df[M_INDEX] = grouped_df[M_INDEX].round(decimals=2)

        return grouped_df

    # -------------------------------------------------------------------------
    def _rank_by_lcs(self, grouped_df):

        grouped_df = grouped_df.copy()

        columns = SELECTED_COLUMNS[LCS]
        ascending = [False] * (len(columns) - 1) + [True]

        grouped_df["_name_"] = grouped_df.index.tolist()
        grouped_df = grouped_df.sort_values(columns, ascending=ascending)
        grouped_df = grouped_df.drop(columns=["_name_"])

        grouped_df.insert(0, RANK_LCS, range(1, len(grouped_df) + 1))

        return grouped_df

    # -------------------------------------------------------------------------
    def _rank_by_gcs(self, grouped_df):

        grouped_df = grouped_df.copy()

        columns = SELECTED_COLUMNS[GCS]
        ascending = [False] * (len(columns) - 1) + [True]

        grouped_df["_name_"] = grouped_df.index.tolist()
        grouped_df = grouped_df.sort_values(columns, ascending=ascending)
        grouped_df = grouped_df.drop(columns=["_name_"])

        grouped_df.insert(0, RANK_GCS, range(1, len(grouped_df) + 1))

        return grouped_df

    # -------------------------------------------------------------------------
    def _rank_by_occ(self, grouped_df):

        grouped_df = grouped_df.copy()

        columns = SELECTED_COLUMNS[OCC]
        ascending = [False] * (len(columns) - 1) + [True]

        grouped_df["_name_"] = grouped_df.index.tolist()
        grouped_df = grouped_df.sort_values(columns, ascending=ascending)
        grouped_df = grouped_df.drop(columns=["_name_"])

        grouped_df.insert(0, RANK_OCC, range(1, len(grouped_df) + 1))

        return grouped_df

    # -------------------------------------------------------------------------
    def _filter_by_item_occurrence_range(self, grouped_df):

        grouped_df = grouped_df.copy()

        if self.params.item_occurrences_range is None:
            return grouped_df

        min_value, max_value = self.params.item_occurrences_range

        if min_value is not None:
            grouped_df = grouped_df[grouped_df[OCC] >= min_value]
        if max_value is not None:
            grouped_df = grouped_df[grouped_df[OCC] <= max_value]

        return grouped_df

    # -------------------------------------------------------------------------
    def _filter_by_item_citations_range(self, grouped_df):

        grouped_df = grouped_df.copy()

        if self.params.item_citations_range is None:
            return grouped_df

        min_value, max_value = self.params.item_citations_range

        if min_value is not None:
            grouped_df = grouped_df[grouped_df[GCS] >= min_value]
        if max_value is not None:
            grouped_df = grouped_df[grouped_df[GCS] <= max_value]

        return grouped_df

    # -------------------------------------------------------------------------
    def _filter_by_items_in(self, grouped_df):

        grouped_df = grouped_df.copy()

        if self.params.items_in is None:
            return grouped_df

        if self.params.items_in is not None:
            #
            items_in = [t for t in self.params.items_in if t in grouped_df.index]
            #
            grouped_df = grouped_df.loc[items_in, :]

        return grouped_df

    # -------------------------------------------------------------------------
    def _filter_by_top_n_items(self, grouped_df):

        columns = SELECTED_COLUMNS[self.params.items_order_by.value]
        ascending = [False] * (len(columns) - 1) + [True]

        grouped_df["_name_"] = grouped_df.index.tolist()
        grouped_df = grouped_df.sort_values(columns, ascending=ascending)
        grouped_df = grouped_df.drop(columns=["_name_"])

        if self.params.top_n is not None:
            grouped_df = grouped_df.head(self.params.top_n)

        return grouped_df

    # -------------------------------------------------------------------------
    def _check_column_types(self, grouped_df):

        grouped_df = grouped_df.copy()

        if OCC in grouped_df.columns:
            grouped_df[OCC] = grouped_df[OCC].astype(int)

        if GCS in grouped_df.columns:
            grouped_df[GCS] = grouped_df[GCS].astype(int)

        if LCS in grouped_df.columns:
            grouped_df[LCS] = grouped_df[LCS].astype(int)

        if H_INDEX in grouped_df.columns:
            grouped_df[H_INDEX] = grouped_df[H_INDEX].astype(int)

        if G_INDEX in grouped_df.columns:
            grouped_df[G_INDEX] = grouped_df[G_INDEX].astype(int)

        return grouped_df

    # -------------------------------------------------------------------------
    def _create_counters_column(self, grouped_df):

        from tm2p._intern.get_zero_digits import get_zero_digits

        occ_zeros, gcs_zeros = get_zero_digits(
            root_directory=self.params.root_directory
        )

        grouped_df = grouped_df.copy()
        grouped_df[COUNTERS] = grouped_df.index.astype(str)

        grouped_df[COUNTERS] += " " + grouped_df[OCC].map(
            lambda x: f"{x:0{occ_zeros}d}"
        )

        grouped_df[COUNTERS] += ":" + grouped_df[GCS].map(
            lambda x: f"{x:0{gcs_zeros}d}"
        )

        return grouped_df

    # -------------------------------------------------------------------------
    def run(self):

        df = self._load_filtered_main_csv_zip()
        df = self._explode_source_field(df)
        df = self._filter_stopitems(df)

        df, grouped_df = self._compute_primary_bibliometric_indicators(df)

        grouped_df = self._compute_derived_bibliometric_indicators(grouped_df)

        grouped_df = self._compute_h_index(df, grouped_df)
        grouped_df = self._compute_g_index(df, grouped_df)
        grouped_df = self._compute_m_index(df, grouped_df)

        grouped_df = self._rank_by_lcs(grouped_df)
        grouped_df = self._rank_by_gcs(grouped_df)
        grouped_df = self._rank_by_occ(grouped_df)

        grouped_df = self._filter_by_item_occurrence_range(grouped_df)
        grouped_df = self._filter_by_item_citations_range(grouped_df)
        grouped_df = self._filter_by_items_in(grouped_df)
        grouped_df = self._filter_by_top_n_items(grouped_df)

        grouped_df = self._check_column_types(grouped_df)

        grouped_df = self._create_counters_column(grouped_df)

        return grouped_df
