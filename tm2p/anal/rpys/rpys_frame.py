"""
RPYS (Reference Publication Year Spectroscopy) Frame
===============================================================================

Smoke tests:
    >>> from tm2p.anal.rpys import RPYSDataFrame
    >>> (
    ...     RPYSDataFrame()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... ).head()
          Num References  Median
    2015               1    -1.0
    2016               7    -7.0
    2017              10   -10.0
    2018              17   -17.0
    2019              15    -5.0



"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class RPYSDataFrame(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        references = load_filtered_main_csv_zip(params=self.params)

        references = references[["year"]]
        references = references.dropna()
        references_by_year = references["year"].value_counts()

        year_min = references_by_year.index.min()
        year_max = references_by_year.index.max()
        years = list(range(year_min, year_max + 1))

        indicator = pd.DataFrame(
            {
                "Num References": 0,
            },
            index=years,
        )

        indicator.loc[references_by_year.index, "Num References"] = references_by_year
        indicator = indicator.sort_index(axis=0, ascending=True)
        indicator["Median"] = (
            indicator["Num References"].rolling(window=5).median().fillna(0)
        )

        indicator["Median"] = indicator["Median"] - indicator["Num References"]

        return indicator
