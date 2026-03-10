"""
Data Frame
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.topic_trends.scientopy.topic_dynamics import TopicDynamics
    >>> df = (
    ...     TopicDynamics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # TIME WINDOW:
    ...     .with_time_window(2)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())  # doctest: +NORMALIZE_WHITESPACE
                          RANK_OCC  RANK_GCS  RANK_LCS  OCC    GCS  LCS  YEAR_FIRST  YEAR_LAST  AGE  GCS_PER_YEAR  LCS_PER_YEAR  GCS_PER_DOC  LCS_PER_DOC  H_INDEX  G_INDEX  M_INDEX                        COUNTERS  BEFORE  BETWEEN  GROWTH_PERCENTAGE  AVERAGE_GROWTH_RATE  AVERAGE_DOCS_PER_YEAR
    AUTHKW_NORM
    fintech                      1         1         1  117  25478    0        2016       2024    9   2830.888889           0.0   217.760684          0.0       97       17    10.78               fintech 117:25478      83       34              29.06                  2.0                   17.0
    financial inclusion          2         2         2   17   3823    0        2016       2024    9    424.777778           0.0   224.882353          0.0       17       11     1.89   financial inclusion 017:03823      12        5              29.41                 -1.0                    2.5
    financial technology         3         5         5   14   2508    0        2016       2024    9    278.666667           0.0   179.142857          0.0       13       10     1.44  financial technology 014:02508      11        3              21.43                  1.0                    1.5
    green finance                4         3         3   11   2844    0        2021       2024    4    711.000000           0.0   258.545455          0.0       11       10     2.75         green finance 011:02844       6        5              45.45                 -1.5                    2.5
    blockchain                   5         7         7   11   2023    0        2016       2024    9    224.777778           0.0   183.909091          0.0       11        8     1.22            blockchain 011:02023       8        3              27.27                  1.0                    1.5



"""

#
# tm2p+ computes three growth indicators for each item in a field (usually
# keywords or noun phrases):
#
# * Average growth rate (AGR):
#
# .. code-block::
#
#            sum_{i=Y_start}^Y_end  Num_Documents[i] - Num_Documents[i-1]
#     AGR = --------------------------------------------------------------
#                             Y_end - Y_start + 1
#
#
# * Average documents per year (ADY):
#
# .. code-block::
#
#            sum_{i=Y_start}^Y_end  Num_Documents[i]
#     ADY = -----------------------------------------
#                     Y_end - Y_start + 1
#
#
# * Percentage of documents in last year (PDLY):
#
# .. code-block::
#
#            sum_{i=Y_start}^Y_end  Num_Documents[i]      1
#     PDLY = ---------------------------------------- * _____
#                   Y_end - Y_start + 1                  TND
#
# With:
#
# .. code-block::
#
#     Y_start = Y_end - time_window + 1
#
# If ``Y_end = 2018`` and ``time_window = 2``, then ``Y_start = 2017``.
#
from tm2p._intern import ParamsMixin
from tm2p.anal.metrics import Metrics

from ...trends import Trends


class TopicDynamics(
    ParamsMixin,
):
    """:meta private:"""

    # ----------------------------------------------------------------------------------------------------
    def _step_1_compute_performance_metrics(self):
        return Metrics().update(**self.params.__dict__).run()

    # ----------------------------------------------------------------------------------------------------
    def _step_2_compute_terms_by_year(self):
        trends = Trends()
        trends = trends.update(**self.params.__dict__)
        trends = trends.using_counters(False)
        df = trends.run()
        return df

    # ----------------------------------------------------------------------------------------------------
    def _step_3_compute_years_by_period(self, terms_by_year):

        time_window = self.params.time_window
        year_start = terms_by_year.columns.min()
        year_end = terms_by_year.columns.max()

        if year_end - year_start + 1 <= time_window:
            raise ValueError(
                "Time window must be less than the number of years in the database"
            )

        first_period_years = list(range(year_start, year_end - time_window + 1))
        last_period_years = list(range(year_end - time_window + 1, year_end + 1))

        return first_period_years, last_period_years

    # ----------------------------------------------------------------------------------------------------
    def _step_4_generate_first_period_occ(
        self,
        terms_by_year,
        first_period_years,
        performance_metrics_data_frame,
    ):

        mapping = terms_by_year.loc[:, first_period_years].sum(axis=1)
        mapping = dict(zip(mapping.index, mapping))

        performance_metrics_data_frame = performance_metrics_data_frame.assign(
            before=performance_metrics_data_frame.index.map(mapping)
        )
        return performance_metrics_data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_5_generate_last_period_occ(
        self,
        terms_by_year,
        last_period_years,
        performance_metrics_data_frame,
    ):
        mapping = terms_by_year.loc[:, last_period_years].sum(axis=1)
        mapping = dict(zip(mapping.index, mapping))

        performance_metrics_data_frame = performance_metrics_data_frame.assign(
            between=performance_metrics_data_frame.index.map(mapping)
        )

        return performance_metrics_data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_6_compute_growth_percentage(
        self,
        performance_metrics_data_frame,
    ):
        performance_metrics_data_frame = performance_metrics_data_frame.assign(
            growth_percentage=(
                (
                    100
                    * performance_metrics_data_frame["between"]
                    / (
                        performance_metrics_data_frame["between"]
                        + performance_metrics_data_frame["before"]
                    )
                ).round(2)
            )
        )

        return performance_metrics_data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_7_compute_average_growth_rate(
        self,
        performance_metrics_data_frame,
        terms_by_year,
        last_period_years,
    ):
        time_window = self.params.time_window

        terms_by_year = terms_by_year.copy()
        diff_terms_by_year = terms_by_year.diff(axis=1)
        diff_terms_by_year = diff_terms_by_year.loc[:, last_period_years]
        diff_terms_by_year = diff_terms_by_year.sum(axis=1) / time_window

        mapping = dict(zip(diff_terms_by_year.index, diff_terms_by_year))

        performance_metrics_data_frame = performance_metrics_data_frame.assign(
            average_growth_rate=(
                (performance_metrics_data_frame.index.map(mapping)).round(2)
            )
        )

        return performance_metrics_data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_8_compute_average_docs_per_year(
        self,
        performance_metrics_data_frame,
        terms_by_year,
        last_period_years,
    ):
        time_window = self.params.time_window

        terms_by_year = terms_by_year.copy()
        terms_by_year = terms_by_year.loc[:, last_period_years]
        terms_by_year = terms_by_year.sum(axis=1) / time_window

        mapping = dict(zip(terms_by_year.index, terms_by_year))

        performance_metrics_data_frame = performance_metrics_data_frame.assign(
            average_docs_per_year=(
                (performance_metrics_data_frame.index.map(mapping)).round(2)
            )
        )

        return performance_metrics_data_frame

    # ----------------------------------------------------------------------------------------------------
    def run(self):

        performance_metrics_data_frame = self._step_1_compute_performance_metrics()

        terms_by_year = self._step_2_compute_terms_by_year()

        first_period_years, last_period_years = self._step_3_compute_years_by_period(
            terms_by_year,
        )

        performance_metrics_data_frame = self._step_4_generate_first_period_occ(
            terms_by_year,
            first_period_years,
            performance_metrics_data_frame,
        )

        performance_metrics_data_frame = self._step_5_generate_last_period_occ(
            terms_by_year,
            last_period_years,
            performance_metrics_data_frame,
        )

        performance_metrics_data_frame = self._step_6_compute_growth_percentage(
            performance_metrics_data_frame,
        )

        performance_metrics_data_frame = self._step_7_compute_average_growth_rate(
            performance_metrics_data_frame,
            terms_by_year,
            last_period_years,
        )

        performance_metrics_data_frame = self._step_8_compute_average_docs_per_year(
            performance_metrics_data_frame,
            terms_by_year,
            last_period_years,
        )

        performance_metrics_data_frame = performance_metrics_data_frame.rename(
            columns={
                "before": "BEFORE",
                "between": "BETWEEN",
                "growth_percentage": "GROWTH_PERCENTAGE",
                "average_growth_rate": "AVERAGE_GROWTH_RATE",
                "average_docs_per_year": "AVERAGE_DOCS_PER_YEAR",
            }
        )

        return performance_metrics_data_frame


#
