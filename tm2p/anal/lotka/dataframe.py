"""
Dataframe
===============================================================================

Smoke tests:
    >>> from tm2p.anal.lotka import DataFrame

    >>> df = (
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
    >>> df
       Documents Written  ...  Prop Theoretical Authors
    0                  1  ...                     0.714
    1                  2  ...                     0.178
    2                  3  ...                     0.079
    3                  5  ...                     0.029
    <BLANKLINE>
    [4 rows x 5 columns]

"""

from tm2p import Field, ItemsOrderBy
from tm2p._intern import ParamsMixin
from tm2p._intern.indic import BibliometricIndicators


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
            BibliometricIndicators()
            .update(**self.params.__dict__)
            .with_source_field(Field.AUTH_NORM)
            .having_items_ordered_by(ItemsOrderBy.OCC)
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
