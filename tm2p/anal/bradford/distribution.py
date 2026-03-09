"""
Distribution
===============================================================================

Smoke tests:
    >>> from tm2p.anal.bradford import Distribution
    >>> df = (
    ...     Distribution()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.to_string())  # doctest: +NORMALIZE_WHITESPACE
       N_SRC PERCENTAGE  ACUM_NUM_SOURCES PERCENTAGE_ACUM  DOCS_PUBLISHED  TOT_DOCS_PUBLISHED  N_DOCS TOT_DOCS  ZONE
    0      1     0.83 %                 1          0.83 %               7                   7       7   3.89 %     1
    1      1     0.83 %                 2          1.65 %               6                   6      13   7.22 %     1
    2      2     1.65 %                 4          3.31 %               5                  10      23  12.78 %     1
    3      3     2.48 %                 7          5.79 %               4                  12      35  19.44 %     1
    4      3     2.48 %                10          8.26 %               3                   9      44  24.44 %     1
    5     25    20.66 %                35         28.93 %               2                  50      94  52.22 %     2
    6     86    71.07 %               121         100.0 %               1                  86     180  100.0 %     3


"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.enum import Field

SRC_ISO4_NORM = Field.SRC_ISO4_NORM.value


class Distribution(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _compute_num_docs_published_by_source(self, df):

        df["num_documents"] = 1

        sources = df.groupby(SRC_ISO4_NORM, as_index=True).agg(
            {
                "num_documents": "sum",
            }
        )
        sources = sources[["num_documents"]]
        sources = sources.groupby(["num_documents"]).size()
        w = [str(round(100 * a / sum(sources), 2)) + " %" for a in sources]
        sources = pd.DataFrame(
            {
                "Num Sources": sources.tolist(),
                "%": w,
                "Documents published": sources.index,
            }
        )

        sources = sources.sort_values(["Documents published"], ascending=False)

        return sources

    # -------------------------------------------------------------------------
    def _compute_bradford_zone_groups(self, df, sources):

        sources = sources.copy()

        sources.loc[:, "Acum Num Sources"] = sources["Num Sources"].cumsum()
        sources["% Acum"] = [
            str(round(100 * a / sum(sources["Num Sources"]), 2)) + " %"
            for a in sources["Acum Num Sources"]
        ]

        sources["Tot Documents published"] = (
            sources["Num Sources"] * sources["Documents published"]
        )
        sources["Num Documents"] = sources["Tot Documents published"].cumsum()
        sources["Tot Documents"] = sources["Num Documents"].map(
            lambda w: str(round(w / sources["Num Documents"].max() * 100, 2)) + " %"
        )

        bradford1 = int(len(df) / 3)
        bradford2 = 2 * bradford1

        sources["Bradford's Group"] = sources["Num Documents"].map(
            lambda w: 3 if w > bradford2 else (2 if w > bradford1 else 1)
        )

        sources = sources[
            [
                "Num Sources",
                "%",
                "Acum Num Sources",
                "% Acum",
                "Documents published",
                "Tot Documents published",
                "Num Documents",
                "Tot Documents",
                "Bradford's Group",
            ]
        ]

        sources = sources.reset_index(drop=True)

        sources = sources.rename(
            columns={
                "Num Sources": "N_SRC",
                "%": "PERCENTAGE",
                "Acum Num Sources": "ACUM_NUM_SOURCES",
                "% Acum": "PERCENTAGE_ACUM",
                "Documents published": "DOCS_PUBLISHED",
                "Tot Documents published": "TOT_DOCS_PUBLISHED",
                "Num Documents": "N_DOCS",
                "Tot Documents": "TOT_DOCS",
                "Bradford's Group": "ZONE",
            }
        )

        return sources

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        df = load_filtered_main_csv_zip(params=self.params)
        sources = self._compute_num_docs_published_by_source(df)
        sources = self._compute_bradford_zone_groups(df, sources)

        return sources


#

#
#
