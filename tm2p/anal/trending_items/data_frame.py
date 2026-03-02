"""
Data Frame
===============================================================================

Smoke tests:
    >>> from tm2p.analyze.metrics.trending_terms.user import DataFrame

    >>> # Create, configure, and run the DataFrame generator
    >>> generator = (
    ...     DataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_field("author_keywords_raw")
    ...     .having_items_in_top(20)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # TIME WINDOW:
    ...     .with_time_window(2)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ... )
    >>> df = generator.run()
    >>> df.head()
                          rank_occ  ...  average_docs_per_year
    author_keywords_raw             ...
    FINTECH                      1  ...                    9.0
    INNOVATION                   2  ...                    0.5
    FINANCIAL_SERVICES           3  ...                    1.5
    FINANCIAL_INCLUSION          4  ...                    0.0
    FINANCIAL_TECHNOLOGY         5  ...                    1.0
    <BLANKLINE>
    [5 rows x 22 columns]



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
from tm2p.anal._intern.performance import (
    PerformanceMetrics as PerformanceMetricsDataFrame,
)

from ..items_by_year import ItemsByYear as TermsByYearDataFrame


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # ----------------------------------------------------------------------------------------------------
    def _step_1_compute_performance_metrics(self):
        return PerformanceMetricsDataFrame().update(**self.params.__dict__).run()

    # ----------------------------------------------------------------------------------------------------
    def _step_2_compute_terms_by_year(self):
        df = TermsByYearDataFrame()
        df = df.update(**self.params.__dict__)
        df = df.using_item_counters(False)
        df = df.run()
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

        return performance_metrics_data_frame


#
