"""
Distribution
===============================================================================

Smoke tests:
    >>> from tm2p.anal.lotka import Distribution

    >>> df = (
    ...     Distribution()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.to_string())  # doctest: +NORMALIZE_WHITESPACE
       DOC_WRITTEN  N_AUTH  AUTH_PROP  N_AUTH_THEO  PROP_AUTH_THEO
    0            1     425      0.897      425.000           0.714
    1            2      41      0.086      106.250           0.178
    2            3       7      0.015       47.222           0.079
    3            5       1      0.002       17.000           0.029



"""

from tm2p import Field, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.anal.metrics import Metrics


class Distribution(
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
            Metrics()
            .update(**self.params.__dict__)
            .with_source_field(Field.AUTH_NORM)
            .having_items_ordered_by(ItemOrderBy.OCC)
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

        indicators = indicators.rename(
            columns={
                "Documents Written": "DOC_WRITTEN",
                "Num Authors": "N_AUTH",
                "Proportion of Authors": "AUTH_PROP",
                "Theoretical Num Authors": "N_AUTH_THEO",
                "Prop Theoretical Authors": "PROP_AUTH_THEO",
            }
        )

        return indicators

    # -------------------------------------------------------------------------
    def run(self):
        self.internal__compute_number_of_written_documents_per_number_of_authors()
        metrics = self.internal__compute_the_theoretical_number_of_authors()
        return metrics


#

#
