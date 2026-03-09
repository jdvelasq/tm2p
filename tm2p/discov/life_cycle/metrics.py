"""
Metrics
===============================================================================

Smoke test:
    >>> from tm2p.discov.life_cycle import Metrics
    >>> df = (
    ...     Metrics()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> isinstance(df.index, pd.MultiIndex)
    True
    >>> len(df) > 0
    True
    >>> df  # doctest: +NORMALIZE_WHITESPACE
                                                                   VALUE
    CATEGORY       ITEM
    MODEL OVERIEW  Saturation (K)                                    384
                   Peak year (t0)                                   2023
                   Peak annual (pubs/yr)                            46.5
                   Growth duration (yrs)                             9.1
    FIT QUALITY    R²                                             0.9956
                   RMSE                                             6.14
                   AIC                                             42.29
    CURRENT STATUS Last observed year                               2025
                   Annual publications                                49
                   Cumulative total                                  286
                   Progress to saturation                          74.55
    MILESTONES     10% of K                                         2018
                   50% of K  (midpoint)                             2023
                   90% of K                                         2027
                   99% of K                                         2032
    FORECAST       2030  (+5 yrs)           372 cum | 7 ann | 96.9% of K
                   2035 (+10 yrs)           383 cum | 1 ann | 99.7% of K
                   2040 (+15 yrs)          384 cum | 0 ann | 100.0% of K



"""

from dataclasses import dataclass, field
from typing import Union

import numpy as np
import pandas as pd  # type: ignore
from sklearn.metrics import mean_squared_error, r2_score  # type: ignore

from tm2p._intern import ParamsMixin

from ._intern.compute_model_parameters import compute_model_parameters
from ._intern.logistic import logistic


@dataclass
class Stats:
    """:meta private:"""

    category: list = field(default_factory=list)
    item: list = field(default_factory=list)
    value: list = field(default_factory=list)


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    def insert_stats(
        self, stats: Stats, category: str, item: str, value: Union[int, float, str]
    ):
        stats.category.append(category)
        stats.item.append(item)
        stats.value.append(value)
        return stats

    def run(self):

        stats = Stats()

        #
        # Model estimation
        #
        K, r, t0, years, annual_counts, cumulative = compute_model_parameters(
            params=self.params
        )
        cum_pred = logistic(years, K, r, t0)

        # =====================================================================
        #
        # MODEL OVERVIEW
        #
        # =====================================================================

        stats = self.insert_stats(
            stats,
            category="MODEL OVERIEW",
            item="Saturation (K)",
            value=f"{K:,.0f}",
        )

        # ---------------------------------------------------------------------

        stats = self.insert_stats(
            stats,
            category="MODEL OVERIEW",
            item="Peak year (t0)",
            value=f"{round(t0)}",
        )

        # ---------------------------------------------------------------------

        peak_annual = (K * r) / 4

        stats = self.insert_stats(
            stats,
            category="MODEL OVERIEW",
            item="Peak annual (pubs/yr)",
            value=f"{peak_annual:.1f}",
        )

        # ---------------------------------------------------------------------

        t_10 = t0 - np.log(9) / r
        t_90 = t0 + np.log(9) / r
        growth_duration = t_90 - t_10

        stats = self.insert_stats(
            stats,
            category="MODEL OVERIEW",
            item="Growth duration (yrs)",
            value=f"{growth_duration:.1f}",
        )

        # =====================================================================
        #
        # FIT QUALITY
        #
        # =====================================================================

        r2 = r2_score(cumulative, cum_pred)

        stats = self.insert_stats(
            stats,
            category="FIT QUALITY",
            item="R²",
            value=f"{r2:.4f}",
        )

        # ---------------------------------------------------------------------

        rmse = np.sqrt(mean_squared_error(cumulative, cum_pred))

        stats = self.insert_stats(
            stats,
            category="FIT QUALITY",
            item="RMSE",
            value=f"{rmse:.2f}",
        )

        # ---------------------------------------------------------------------

        n, k = len(years), 3
        rss = np.sum((cumulative - cum_pred) ** 2)
        aic = n * np.log(rss / n) + 2 * k

        stats = self.insert_stats(
            stats,
            category="FIT QUALITY",
            item="AIC",
            value=f"{aic:.2f}",
        )

        # =====================================================================
        #
        # CURRENT STATUS
        #
        # =====================================================================

        last_year = int(years[-1])

        stats = self.insert_stats(
            stats,
            category="CURRENT STATUS",
            item="Last observed year",
            value=f"{last_year}",
        )

        # ---------------------------------------------------------------------

        last_annual = int(annual_counts[-1])

        stats = self.insert_stats(
            stats,
            category="CURRENT STATUS",
            item="Annual publications",
            value=f"{last_annual:,}",
        )

        # ---------------------------------------------------------------------

        cum_total = int(cumulative[-1])

        stats = self.insert_stats(
            stats,
            category="CURRENT STATUS",
            item="Cumulative total",
            value=f"{cum_total:,}",
        )

        # ---------------------------------------------------------------------

        saturation_pct = (cumulative[-1] / K) * 100

        stats = self.insert_stats(
            stats,
            category="CURRENT STATUS",
            item="Progress to saturation",
            value=f"{saturation_pct:.2f}",
        )

        # ---------------------------------------------------------------------

        # progress_pct = saturation_pct

        # =====================================================================
        #
        # MILESTONE YEARS
        #
        # =====================================================================

        def year_at_pct(pct):
            p = pct / 100
            return round(t0 - np.log(1 / p - 1) / r)

        milestone_10 = year_at_pct(10)
        milestone_50 = year_at_pct(50)
        milestone_90 = year_at_pct(90)
        milestone_99 = year_at_pct(99)

        stats = self.insert_stats(
            stats,
            category="MILESTONES",
            item="10% of K",
            value=f"{milestone_10}",
        )

        stats = self.insert_stats(
            stats,
            category="MILESTONES",
            item="50% of K  (midpoint)",
            value=f"{milestone_50}",
        )

        stats = self.insert_stats(
            stats,
            category="MILESTONES",
            item="90% of K",
            value=f"{milestone_90}",
        )

        stats = self.insert_stats(
            stats,
            category="MILESTONES",
            item="99% of K",
            value=f"{milestone_99}",
        )

        # =====================================================================
        #
        # FORECASTS
        #
        # =====================================================================

        def forecast(offset):
            t_fut = last_year + offset
            cum_fut = logistic(t_fut, K, r, t0)
            ann_fut = logistic(t_fut, K, r, t0) - logistic(t_fut - 1, K, r, t0)
            pct_fut = (cum_fut / K) * 100
            return round(cum_fut), round(ann_fut), f"{pct_fut:.1f}%"

        f5_cum, f5_ann, f5_pct = forecast(5)
        f10_cum, f10_ann, f10_pct = forecast(10)
        f15_cum, f15_ann, f15_pct = forecast(15)

        stats = self.insert_stats(
            stats,
            category="FORECAST",
            item=f"{last_year + 5}  (+5 yrs)",
            value=f"{f5_cum:,} cum | {f5_ann:,} ann | {f5_pct} of K",
        )

        stats = self.insert_stats(
            stats,
            category="FORECAST",
            item=f"{last_year + 10} (+10 yrs)",
            value=f"{f10_cum:,} cum | {f10_ann:,} ann | {f10_pct} of K",
        )

        stats = self.insert_stats(
            stats,
            category="FORECAST",
            item=f"{last_year + 15} (+15 yrs)",
            value=f"{f15_cum:,} cum | {f15_ann:,} ann | {f15_pct} of K",
        )

        # =====================================================================
        #
        # REPORT
        #
        # =====================================================================

        df = pd.DataFrame(
            {
                "CATEGORY": stats.category,
                "ITEM": stats.item,
                "VALUE": stats.value,
            }
        )
        df = df.set_index(["CATEGORY", "ITEM"])

        return df
