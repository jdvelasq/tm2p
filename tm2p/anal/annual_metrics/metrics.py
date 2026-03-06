"""
DataFrame
===============================================================================

Smoke tests:
    >>> from tm2p.anal.annual_metrics.metrics import Metrics
    >>> df = (
    ...     Metrics()
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 0
    True
    >>> print(df.to_string())  # doctest: +NORMALIZE_WHITESPACE
          OCC  CUMUL_OCC  CITAB_YEAR   GCS  CUMUL_GCS   MEAN_GCS  MEAN_GCS_PER_YEAR  LCS  CUMUL_LCS  MEAN_LCS  MEAN_LCS_PER_YEAR
    YEAR
    2016    3          3          10   212        212  70.666667               7.07    0          0       0.0                0.0
    2017    7         10           9   481        693  68.714286               7.63    0          0       0.0                0.0
    2018   22         32           8   986       1679  44.818182               5.60    0          0       0.0                0.0
    2019   20         52           7   999       2678  49.950000               7.14    0          0       0.0                0.0
    2020   29         81           6  1456       4134  50.206897               8.37    0          0       0.0                0.0
    2021   34        115           5   639       4773  18.794118               3.76    0          0       0.0                0.0
    2022   35        150           4   515       5288  14.714286               3.68    0          0       0.0                0.0
    2023   39        189           3   496       5784  12.717949               4.24    0          0       0.0                0.0
    2024   48        237           2   216       6000   4.500000               2.25    0          0       0.0                0.0
    2025   49        286           1    57       6057   1.163265               1.16    0          0       0.0                0.0



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

from .column import Column

GCS = Column.GCS.value
LCS = Column.LCS.value
YEAR = Column.YEAR.value
OCC = Column.OCC.value
CUMUL_OCC = Column.CUMUL_OCC.value
CUMUL_LCS = Column.CUMUL_LCS.value
CITAB_YEAR = Column.CITAB_YEAR.value
MEAN_LCS_PER_YEAR = Column.MEAN_LCS_PER_YEAR.value
MEAN_GCS_PER_YEAR = Column.MEAN_GCS_PER_YEAR.value

MEAN_GCS = Column.MEAN_GCS.value
MEAN_LCS = Column.MEAN_LCS.value
CUMUL_GCS = Column.CUMUL_GCS.value


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    def _select_columns(self, df):

        df = df.copy()

        columns = [
            YEAR,
            GCS,
            LCS,
        ]
        df = df[columns]
        df[OCC] = 1
        df[YEAR] = df[YEAR].astype(int)

        return df

    def _group_by_year_and_sort(self, df):

        df = df.groupby(YEAR, as_index=True).sum()
        df = df.sort_index(ascending=True, axis=0)

        return df

    def _compute_cumulated_documents(self, df):

        df[CUMUL_OCC] = df[OCC].cumsum()

        return df

    def _compute_citable_years(self, df):

        current_year = df.index.max()
        df[CITAB_YEAR] = current_year - df.index + 1

        return df

    def _compute_global_citation_metrics(self, df):

        df[MEAN_GCS] = df[GCS] / df[OCC]
        df[CUMUL_GCS] = df[GCS].cumsum()
        df[MEAN_GCS_PER_YEAR] = df[MEAN_GCS] / df[CITAB_YEAR]
        df[MEAN_GCS_PER_YEAR] = df[MEAN_GCS_PER_YEAR].round(2)

        return df

    def _compute_local_citation_metrics(self, df):

        df[MEAN_LCS] = df[LCS] / df[OCC]
        df[CUMUL_LCS] = df[LCS].cumsum()
        df[MEAN_LCS_PER_YEAR] = df[MEAN_LCS] / df[CITAB_YEAR]
        df[MEAN_LCS_PER_YEAR] = df[MEAN_LCS_PER_YEAR].round(2)

        return df

    def _reorder_columns(self, df):

        return df[
            [
                OCC,
                CUMUL_OCC,
                CITAB_YEAR,
                GCS,
                CUMUL_GCS,
                MEAN_GCS,
                MEAN_GCS_PER_YEAR,
                LCS,
                CUMUL_LCS,
                MEAN_LCS,
                MEAN_LCS_PER_YEAR,
            ]
        ]

    def run(self):

        df = load_filtered_main_csv_zip(params=self.params)

        df = self._select_columns(df)
        df = self._group_by_year_and_sort(df)
        df = self._compute_cumulated_documents(df)
        df = self._compute_citable_years(df)
        df = self._compute_global_citation_metrics(df)
        df = self._compute_local_citation_metrics(df)
        df = self._reorder_columns(df)

        return df
