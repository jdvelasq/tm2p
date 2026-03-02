"""
Dataframe
===============================================================================

Smoke tests:
    >>> from tm2p.analyze.metrics.lotka_law import DataFrame

    >>> generator = (
    ...     DataFrame()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ... )
    >>> df = generator.run()
    >>> df
       Documents Written  ...  Prop Theoretical Authors
    0                  1  ...                     0.735
    1                  2  ...                     0.184
    2                  3  ...                     0.082
    <BLANKLINE>
    [3 rows x 5 columns]

"""

from tm2p._intern import ParamsMixin
from tm2p.anal._intern.performance.performance_metrics import (
    PerformanceMetrics as PerformanceDataFrame,
)


class DataFrame(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__compute_number_of_written_documents_per_number_of_authors(self):
        #
        #  Read as: "178 authors write only 1 document and 1 author writes 7 documents"
        #
        #    Documents Written  Num Authors
        # 0                  1          178
        # 1                  2            9
        # 2                  3            2
        # 3                  4            2
        # 4                  6            1
        # 5                  7            1
        #

        indicators = (
            PerformanceDataFrame()
            .update(**self.params.__dict__)
            .update(field="authors")
            .update(terms_order_by="OCC")
            .run()
        )

        indicators = indicators[["OCC"]]
        indicators = indicators.groupby(["OCC"], as_index=False).size()
        indicators.columns = ["Documents Written", "Num Authors"]
        indicators = indicators.sort_values(by="Documents Written", ascending=True)
        indicators = indicators.reset_index(drop=True)
        indicators = indicators[["Documents Written", "Num Authors"]]
        indicators["Proportion of Authors"] = (
            indicators["Num Authors"]
            .map(lambda x: x / indicators["Num Authors"].sum())
            .round(3)
        )

        self.indicators = indicators

    # -------------------------------------------------------------------------
    def internal__compute_the_theoretical_number_of_authors(self):

        indicators = self.indicators
        total_authors = indicators["Num Authors"].max()
        indicators["Theoretical Num Authors"] = (
            indicators["Documents Written"]
            .map(lambda x: total_authors / float(x * x))
            .round(3)
        )
        total_theoretical_num_authors = indicators["Theoretical Num Authors"].sum()
        indicators["Prop Theoretical Authors"] = (
            indicators["Theoretical Num Authors"]
            .map(lambda x: x / total_theoretical_num_authors)
            .round(3)
        )

        self.indicators = indicators

    # -------------------------------------------------------------------------
    def run(self):
        self.internal__compute_number_of_written_documents_per_number_of_authors()
        self.internal__compute_the_theoretical_number_of_authors()
        return self.indicators


#

#
