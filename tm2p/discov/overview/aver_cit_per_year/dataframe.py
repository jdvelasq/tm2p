"""
DataFrame
===============================================================================

Smoke tests:
    >>> from tm2p.discov.overview.average_citations_per_year import DataFrame
    >>> df = (
    ...     DataFrame()
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 0
    True
    >>> df
             OCC  cum_OCC  ...  mean_local_citations  mean_local_citations_per_year
    PUBYEAR                ...
    2016       3        3  ...              0.000000                           0.00
    2017       7       10  ...              0.000000                           0.00
    2018      22       32  ...              0.090909                           0.01
    2019      20       52  ...              0.250000                           0.04
    2020      29       81  ...              0.931034                           0.16
    2021      34      115  ...              0.411765                           0.08
    2022      35      150  ...              0.685714                           0.17
    2023      39      189  ...              1.153846                           0.38
    2024      48      237  ...              1.041667                           0.52
    2025      49      286  ...              0.918367                           0.92
    <BLANKLINE>
    [10 rows x 11 columns]


"""

from tm2p import Field, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

PUBYEAR = Field.YEAR.value
CIT_COUNT_GLOBAL = ItemOrderBy.GCS.value
CIT_COUNT_LOCAL = ItemOrderBy.LCS.value
CIT_COUNT_GLOBAL_PER_YEAR_AVG = ItemOrderBy.GCS_PER_YEAR_AVG.value


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_1_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def _step_2_select_columns(self, dataframe):
        columns = [PUBYEAR, CIT_COUNT_GLOBAL, CIT_COUNT_LOCAL]
        dataframe = dataframe[columns]
        dataframe = dataframe.assign(OCC=1)
        dataframe[PUBYEAR] = dataframe[PUBYEAR].astype(int)
        return dataframe

    # -------------------------------------------------------------------------
    def _step_3_group_by_year_and_sort(self, dataframe):
        dataframe = dataframe.groupby(PUBYEAR, as_index=True).sum()
        dataframe = dataframe.sort_index(ascending=True, axis=0)
        return dataframe

    # -------------------------------------------------------------------------
    def _step_4_compute_cumulated_documents(self, dataframe):
        dataframe = dataframe.assign(cum_OCC=dataframe.OCC.cumsum())
        dataframe.insert(1, "cum_OCC", dataframe.pop("cum_OCC"))
        return dataframe

    # -------------------------------------------------------------------------
    def _step_5_compute_citable_years(self, dataframe):
        current_year = dataframe.index.max()
        dataframe = dataframe.assign(citable_years=current_year - dataframe.index + 1)
        return dataframe

    # -------------------------------------------------------------------------
    def _step_6_compute_global_citations(self, dataframe):
        dataframe = dataframe.assign(
            mean_global_citations=dataframe[CIT_COUNT_GLOBAL] / dataframe.OCC
        )
        dataframe = dataframe.assign(
            cum_global_citations=dataframe[CIT_COUNT_GLOBAL].cumsum()
        )

        dataframe[CIT_COUNT_GLOBAL_PER_YEAR_AVG] = (
            dataframe.mean_global_citations / dataframe.citable_years
        )
        dataframe[CIT_COUNT_GLOBAL_PER_YEAR_AVG] = dataframe[
            CIT_COUNT_GLOBAL_PER_YEAR_AVG
        ].round(2)

        return dataframe

    # -------------------------------------------------------------------------
    def _step_7_compute_local_citations(self, dataframe):
        dataframe = dataframe.assign(
            mean_local_citations=dataframe[CIT_COUNT_LOCAL] / dataframe.OCC
        )
        dataframe = dataframe.assign(
            cum_local_citations=dataframe[CIT_COUNT_LOCAL].cumsum()
        )
        dataframe = dataframe.assign(
            mean_local_citations_per_year=dataframe.mean_local_citations
            / dataframe.citable_years
        )
        dataframe.mean_local_citations_per_year = (
            dataframe.mean_local_citations_per_year.round(2)
        )
        return dataframe

    # -------------------------------------------------------------------------
    def _step_8_reorder_columns(self, dataframe):
        dataframe = dataframe[
            [
                "OCC",
                "cum_OCC",
                "citable_years",
                CIT_COUNT_GLOBAL,
                "cum_global_citations",
                "mean_global_citations",
                CIT_COUNT_GLOBAL_PER_YEAR_AVG,
                CIT_COUNT_LOCAL,
                "cum_local_citations",
                "mean_local_citations",
                "mean_local_citations_per_year",
            ]
        ]
        return dataframe

    # -------------------------------------------------------------------------
    def run(self):

        data_frame = self._step_1_load_the_database()
        data_frame = self._step_2_select_columns(data_frame)
        data_frame = self._step_3_group_by_year_and_sort(data_frame)
        data_frame = self._step_4_compute_cumulated_documents(data_frame)
        data_frame = self._step_5_compute_citable_years(data_frame)
        data_frame = self._step_6_compute_global_citations(data_frame)
        data_frame = self._step_7_compute_local_citations(data_frame)
        data_frame = self._step_8_reorder_columns(data_frame)

        return data_frame
