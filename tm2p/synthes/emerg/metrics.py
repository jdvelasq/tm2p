"""
Metrics
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.synthes.emerg import Metrics
    >>> df = (
    ...     Metrics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.KW_NORM)
    ...     #
    ...     # EMERGENCE:
    ...     .using_baseline_periods(3)
    ...     .using_recent_periods(3)
    ...     .using_novelty_threshold(0.15)
    ...     .using_total_records_threshold(7)
    ...     .using_periods_with_at_least_one_record(3)
    ...     .using_ratio_threshold(0.5)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.head().to_string())  # doctest: +NORMALIZE_WHITESPACE
                                       OCC  OCC_BASELINE  OCC_RECENT  NONZERO_YEARS   PO  PF  NP  GROWTH_RATE  GROWTH_RATE_RATIO
    KW_NORM
    innovation 020:03916                20             6           9              9  3.0  20   8    26.761857           0.660623
    china 018:03596                     18             1          11              7  1.0  18   8    43.518889           1.074275
    financial inclusion 017:03823       17             4           9              8  1.0  17   8    42.497129           1.049053
    financial technology 015:02583      15             2           4              8  1.0  15   8    40.285055           0.994447
    sustainable development 015:02158   15             1          10              6  1.0  15   8    40.285055           0.994447


"""

import numpy as np

from tm2p import ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.anal.annual_metrics.metrics import Metrics as TrendMetricsDataFrame
from tm2p.anal.trends import Trends
from tm2p.discov.overview import MainInformation as GeneralMetricsDataFrame


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    def _step_1_compute_term_occurrences_by_year(self):

        return (
            Trends()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .using_cumulative_sum(False)
            .run()
        )

    def _step_2_compute_base_indicators(self, occurrences_by_year):
        #
        baseline_periods = self.params.baseline_periods
        recent_periods = self.params.recent_periods
        #
        data_frame = occurrences_by_year.sum(axis=1).to_frame()
        data_frame.columns = ["OCC"]
        data_frame["OCC_BASELINE"] = occurrences_by_year.iloc[:, :baseline_periods].sum(
            axis=1
        )
        data_frame["OCC_RECENT"] = occurrences_by_year.iloc[:, -recent_periods:].sum(
            axis=1
        )
        data_frame["NONZERO_YEARS"] = (occurrences_by_year > 0).sum(axis=1)
        #
        return data_frame

    def _step_3_compute_records_by_bas_period(self):
        baseline_periods = self.params.baseline_periods
        return (
            TrendMetricsDataFrame()
            .update(**self.params.__dict__)
            .run()
            .OCC[:baseline_periods]
            .sum()
        )

    def run(self):

        occurrences_by_year = self._step_1_compute_term_occurrences_by_year()
        data_frame = self._step_2_compute_base_indicators(occurrences_by_year)
        records_by_base_period = self._step_3_compute_records_by_bas_period()
        data_frame["selected"] = True

        #
        # Threshold: The term  appear in 15% or less of the base period records
        #
        novelty_threshold = self.params.novelty_threshold
        data_frame["selected"] = data_frame["selected"] & (
            data_frame["OCC_BASELINE"] / records_by_base_period <= novelty_threshold
        )

        #
        # Threshold: The term appears in at least 'total_records_threshold' records
        #
        total_records_threshold = self.params.total_records_threshold
        data_frame["selected"] = data_frame["selected"] & (
            data_frame["OCC"] >= total_records_threshold
        )

        #
        # Threshold: The term appears in at leat 'periods_with_at_least_one_record' periods
        #
        periods_with_at_least_one_record = self.params.periods_with_at_least_one_record
        data_frame["selected"] = data_frame["selected"] & (
            data_frame["NONZERO_YEARS"] >= periods_with_at_least_one_record
        )

        #
        # Threshold: The growth reate of the terms must be 'ratio_threshold' times
        # of the growth rate of the dataset
        #

        cum_occurrences_by_year = (
            Trends()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .using_cumulative_sum(True)
            .run()
        )

        n_columns = cum_occurrences_by_year.columns.max()

        data_frame["PO"] = cum_occurrences_by_year.where(
            cum_occurrences_by_year > 0, np.inf
        ).min(axis=1)

        data_frame["PF"] = cum_occurrences_by_year.max(axis=1)

        data_frame["NP"] = n_columns - cum_occurrences_by_year.where(
            cum_occurrences_by_year > 0, np.inf
        ).idxmin(axis=1)

        data_frame["GROWTH_RATE"] = 100.0 * (
            np.power(
                data_frame["PF"].astype(float) / data_frame["PO"].astype(float),
                1.0 / data_frame["NP"].astype(float),
            )
            - 1
        )

        global_growth_rate = (
            GeneralMetricsDataFrame()
            .update(**self.params.__dict__)
            .run()
            .loc[("GENERAL", "Annual growth rate %"), "Value"]
        )

        data_frame["GROWTH_RATE_RATIO"] = data_frame["GROWTH_RATE"].map(
            lambda x: x / global_growth_rate
        )

        ratio_threshold = self.params.ratio_threshold
        data_frame["selected"] = data_frame["selected"] & (
            data_frame["GROWTH_RATE_RATIO"] >= ratio_threshold
        )

        # n_years = max(self.records.year) - min(self.records.year) + 1
        # po_ = len(self.records.year[self.records.year == min(self.records.year)])
        # return round(100 * (np.power(self.n_records / po_, 1 / n_years) - 1), 2)

        #
        # NOTE: Used in the first versions of the package
        # Threshold: The ratio of records containing the term in the active period to
        # those in the base period must be at least 'ratio_threshold':1
        #
        # data_frame["selected"] = data_frame["selected"] & (
        #     data_frame["OCC_recent"] / data_frame["OCC_baseline"] >= ratio_threshold
        # )

        return data_frame[data_frame.selected].drop(columns=["selected"])
