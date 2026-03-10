"""
TopicDynamics
===============================================================================

Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.anal.topic_trends.burst.topic_dynamics import TopicDynamics
    >>> df = (
    ...     TopicDynamics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # KLEINBERG BURST:
    ...     .using_kleinberg_burst_rate(2.0)
    ...     .using_kleinberg_burst_gamma(1.0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
                                    LEVEL  START   END  DURATION  OCC
    ITEM
    fintech companies 014:03279         1   2016  2017         1   14
    china 033:06419                     1   2021  2023         2   33
    fintech development 015:03625       1   2021  2022         1   15
    economic growth 012:01976           1   2022  2024         2   12
    financial technology 051:09258      1   2023  2023         0   51


    >>> df = (
    ...     TopicDynamics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.CONCEPT_NORM)
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # KLEINBERG BURST:
    ...     .using_kleinberg_burst_rate(2.0)
    ...     .using_kleinberg_burst_gamma(1.0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +NORMALIZE_WHITESPACE
                          LEVEL  START   END  DURATION  OCC
    ITEM
    fintech companies         1   2016  2017         1   14
    china                     1   2021  2023         2   33
    fintech development       1   2021  2022         1   15
    economic growth           1   2022  2024         2   12
    financial technology      1   2023  2023         0   51


"""

from math import log

import numpy as np
import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin, remove_counters
from tm2p.anal.trends import Trends


class TopicDynamics(
    ParamsMixin,
):
    """:meta private:"""

    def kleinberg_burst_detection(self, timestamps, rate=2.0, gamma=1.0, n=None):
        timestamps = sorted(timestamps)
        if len(timestamps) < 2:
            return [], []

        T = timestamps[-1] - timestamps[0]
        if T == 0:
            return [], []

        num_events = len(timestamps)
        gaps = np.diff(timestamps).astype(float)
        # Add tiny jitter to avoid zero gaps (same-year events)
        gaps = np.where(gaps == 0, 1e-6, gaps)
        m = len(gaps)

        if n is None:
            n = max(2, int(np.ceil(1 + log(num_events, rate))))

        avg_rate = num_events / T
        rates = np.array([avg_rate * (rate**q) for q in range(n)])

        def emit_cost(gap, q):
            return rates[q] * gap - log(rates[q])

        def trans_cost(i, j):
            return max(0, (j - i) * gamma * log(n))

        INF = float("inf")
        cost = np.full((m, n), INF)
        prev = np.zeros((m, n), dtype=int)

        for q in range(n):
            cost[0, q] = emit_cost(gaps[0], q) + trans_cost(0, q)

        for t in range(1, m):
            for q in range(n):
                options = [cost[t - 1, p] + trans_cost(p, q) for p in range(n)]
                best_p = int(np.argmin(options))
                cost[t, q] = options[best_p] + emit_cost(gaps[t], q)
                prev[t, q] = best_p

        states = np.zeros(m, dtype=int)
        states[-1] = np.argmin(cost[-1])
        for t in range(m - 2, -1, -1):
            states[t] = prev[t + 1, states[t + 1]]

        bursts = []
        for level in range(1, n):
            in_burst = False
            start = None
            for t in range(m):
                if states[t] >= level and not in_burst:
                    in_burst = True
                    start = timestamps[t]
                elif states[t] < level and in_burst:
                    bursts.append((level, start, timestamps[t]))
                    in_burst = False
            if in_burst:
                bursts.append((level, start, timestamps[-1]))

        return bursts, states.tolist()

    def counts_to_timestamps(self, series: pd.Series) -> list:

        timestamps = []
        for year, count in series.items():
            if count > 0:
                # Spread events evenly across the year
                offsets = np.linspace(0, 1, int(count) + 2)[1:-1]
                year = float(year)  # type: ignore
                timestamps.extend([year + float(o) for o in offsets])
        return sorted(timestamps)

    def detect_bursts_from_df(self, df):

        scaling = self.params.kleinberg_burst_rate
        gamma = self.params.kleinberg_burst_gamma

        years = [int(c) for c in df.columns]
        df.columns = years

        results = {}
        for item in df.index:
            series = df.loc[item]
            total = series.sum()

            timestamps = self.counts_to_timestamps(series)
            bursts, _ = self.kleinberg_burst_detection(
                timestamps, rate=scaling, gamma=gamma
            )

            if bursts:
                max_level = max(b[0] for b in bursts)
                results[item] = {
                    "bursts": bursts,
                    "max_level": max_level,
                    "total": int(total),
                }

        return results

    def burst_summary_table(self, results, year_start=None, year_end=None):

        rows = []
        for item, data in results.items():
            for level, start, end in data["bursts"]:
                s_yr = int(start)
                e_yr = int(end)
                if year_start and s_yr < year_start:
                    continue
                if year_end and e_yr > year_end:
                    continue
                rows.append(
                    {
                        "item": item,
                        "level": level,
                        "start": s_yr,
                        "end": e_yr,
                        "duration": e_yr - s_yr,
                        "total_occ": data["total"],
                    }
                )

        summary = pd.DataFrame(rows)
        if not summary.empty:
            summary = summary.sort_values(["level", "start"], ascending=[False, True])
        return summary.reset_index(drop=True)

    def run(self):

        use_counters = self.params.counters
        self.params.counters = True
        df = Trends().update(**self.params.__dict__).run()
        results = self.detect_bursts_from_df(df)
        summary = self.burst_summary_table(results)

        summary = summary.rename(
            columns={
                "item": "ITEM",
                "level": "LEVEL",
                "start": "START",
                "end": "END",
                "duration": "DURATION",
                "total_occ": "OCC",
            }
        )

        summary = summary.set_index("ITEM")

        if use_counters is False:
            self.params.counters = False
            summary.index = summary.index.map(remove_counters)

        return summary


#
