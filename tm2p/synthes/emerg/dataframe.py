"""
Data Frame
===============================================================================

Smoke tests:
    >>> from tm2p.packages.emergence import DataFrame
    >>> (
    ...     DataFrame()
    ...     #
    ...     # FIELD:
    ...     .with_field("descriptors")
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
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()  # doctest: +SKIP
                       OCC  OCC_baseline  ...  growth_rate  growth_rate_ratio
    descriptors                           ...
    DATA 07:1086         7             2  ...    87.082869           0.733824
    CONSUMERS 07:0925    7             1  ...   164.575131           1.386830
    <BLANKLINE>
    [2 rows x 10 columns]


"""

import numpy as np

from tm2p._intern import ParamsMixin
from tm2p.discov.overview import MainInformation as GeneralMetricsDataFrame
from tm2p.discov.overview.aver_cit_per_year.dataframe import (
    DataFrame as TrendMetricsDataFrame,
)


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # ----------------------------------------------------------------------------------------------------
    def _step_1_compute_term_occurrences_by_year(self):

        from tm2p.anal._intern.items_by_year import ItemsByYear as TermsByYearDataFrame

        return (
            TermsByYearDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .using_cumulative_sum(False)
            .run()
        )

    # ----------------------------------------------------------------------------------------------------
    def _step_2_compute_base_indicators(self, occurrences_by_year):
        #
        baseline_periods = self.params.baseline_periods
        recent_periods = self.params.recent_periods
        #
        data_frame = occurrences_by_year.sum(axis=1).to_frame()
        data_frame.columns = ["OCC"]
        data_frame["OCC_baseline"] = occurrences_by_year.iloc[:, :baseline_periods].sum(
            axis=1
        )
        data_frame["OCC_recent"] = occurrences_by_year.iloc[:, -recent_periods:].sum(
            axis=1
        )
        data_frame["nonzero_years"] = (occurrences_by_year > 0).sum(axis=1)
        #
        return data_frame

    # ----------------------------------------------------------------------------------------------------
    def _step_3_compute_records_by_bas_period(self):
        baseline_periods = self.params.baseline_periods
        return (
            TrendMetricsDataFrame()
            .update(**self.params.__dict__)
            .run()
            .OCC[:baseline_periods]
            .sum()
        )

    # ----------------------------------------------------------------------------------------------------
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
            data_frame["OCC_baseline"] / records_by_base_period <= novelty_threshold
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
            data_frame["nonzero_years"] >= periods_with_at_least_one_record
        )

        #
        # Threshold: The growth reate of the terms must be 'ratio_threshold' times
        # of the growth rate of the dataset
        #

        cum_occurrences_by_year = (
            TermsByYearDataFrame()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .using_cumulative_sum(True)
            .run()
        )

        n_columns = cum_occurrences_by_year.columns.max()

        data_frame["po"] = cum_occurrences_by_year.where(
            cum_occurrences_by_year > 0, np.inf
        ).min(axis=1)

        data_frame["pf"] = cum_occurrences_by_year.max(axis=1)

        data_frame["np"] = n_columns - cum_occurrences_by_year.where(
            cum_occurrences_by_year > 0, np.inf
        ).idxmin(axis=1)

        data_frame["growth_rate"] = 100.0 * (
            np.power(
                data_frame["pf"].astype(float) / data_frame["po"].astype(float),
                1.0 / data_frame["np"].astype(float),
            )
            - 1
        )

        global_growth_rate = (
            GeneralMetricsDataFrame()
            .update(**self.params.__dict__)
            .run()
            .loc[("GENERAL", "Annual growth rate %"), "Value"]
        )

        data_frame["growth_rate_ratio"] = data_frame["growth_rate"].map(
            lambda x: x / global_growth_rate
        )

        ratio_threshold = self.params.ratio_threshold
        data_frame["selected"] = data_frame["selected"] & (
            data_frame["growth_rate_ratio"] >= ratio_threshold
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

        return data_frame[data_frame.selected]

        return data_frame[data_frame.selected]
