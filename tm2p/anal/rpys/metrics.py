"""
Metrics
===============================================================================

Smoke tests:
    >>> from tm2p.anal.rpys import Metrics
    >>> (
    ...     Metrics()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... ).head()
          N_GCR  MEDIAN
    2015      6    -6.0
    2016     18   -18.0
    2017     19   -19.0
    2018     18   -18.0
    2019     19    -1.0




"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class Metrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        references = load_filtered_main_csv_zip(params=self.params)

        references = references[["YEAR"]]
        references = references.dropna()
        references_by_year = references["YEAR"].value_counts()

        year_min = references_by_year.index.min()
        year_max = references_by_year.index.max()
        years = list(range(year_min, year_max + 1))

        indicator = pd.DataFrame(
            {
                "N_GCR": 0,
            },
            index=years,
        )

        indicator.loc[references_by_year.index, "N_GCR"] = references_by_year
        indicator = indicator.sort_index(axis=0, ascending=True)
        indicator["MEDIAN"] = indicator["N_GCR"].rolling(window=5).median().fillna(0)

        indicator["MEDIAN"] = indicator["MEDIAN"] - indicator["N_GCR"]

        return indicator
