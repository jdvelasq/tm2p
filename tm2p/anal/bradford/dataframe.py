"""
Dataframe
===============================================================================

Smoke tests:
    >>> from tm2p.anal.bradford import DataFrame
    >>> (
    ...     DataFrame()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
       Num Sources        %  ...  Tot Documents Bradford's Group
    0            1   0.83 %  ...         3.89 %                1
    1            1   0.83 %  ...         7.22 %                1
    2            2   1.65 %  ...        12.78 %                1
    3            3   2.48 %  ...        19.44 %                1
    4            3   2.48 %  ...        24.44 %                1
    5           25  20.66 %  ...        52.22 %                2
    6           86  71.07 %  ...        100.0 %                3
    <BLANKLINE>
    [7 rows x 9 columns]

"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.enum import Field

SRC_ISO4_NORM = Field.SRC_ISO4_NORM.value


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def step_1_load_filtered_records(self):
        self.records = load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def step_2_compute_num_docs_published_by_source(self):

        self.records["num_documents"] = 1

        sources = self.records.groupby(SRC_ISO4_NORM, as_index=True).agg(
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

        self.sources = sources

    # -------------------------------------------------------------------------
    def step_3_compute_bradford_zone_groups(self):

        sources = self.sources.copy()

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

        bradford1 = int(len(self.records) / 3)
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

        self.sources = sources

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self.step_1_load_filtered_records()
        self.step_2_compute_num_docs_published_by_source()
        self.step_3_compute_bradford_zone_groups()

        return self.sources


#

#
#
