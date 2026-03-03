"""
Dataframe
===============================================================================


Smoke tests:
    >>> from tmp2 import Corpus
    >>> from tm2p.anal.topic_trends.bibliometrix.topic_dynamics import TopicDynamics
    >>> df = (
    ...     TopicDynamics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .having_terms_per_year(5)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()
    year                      OCC  global_citations  year_q1  ...  rn    height  width
    author_keywords_raw                                       ...
    CONTENT_ANALYSIS 02:0181    2               181     2016  ...   2  0.177333      1
    DIGITALIZATION 02:0181      2               181     2016  ...   3  0.177333      1
    POPULAR_PRESS 02:0181       2               181     2016  ...   4  0.177333      1
    TECHNOLOGY 02:0310          2               310     2016  ...   0  0.177333      2
    BANKING 02:0291             2               291     2016  ...   1  0.177333      2
    <BLANKLINE>
    [5 rows x 8 columns]


    >>> (
    ...     TopicDynamics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .having_terms_per_year(5)
    ...     .having_items_in(
    ...         [
    ...             "FINTECH",
    ...             "BLOCKCHAIN",
    ...             "ARTIFICIAL_INTELLIGENCE",
    ...         ]
    ...     )
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ).head()
    year                             OCC  global_citations  ...  height  width
    author_keywords_raw                                     ...
    FINTECH 31:5168                   31              5168  ...    0.97      2
    BLOCKCHAIN 02:0305                 2               305  ...    0.15      2
    ARTIFICIAL_INTELLIGENCE 02:0327    2               327  ...    0.15      1
    <BLANKLINE>
    [3 rows x 8 columns]


"""

import numpy as np

from tm2p._intern import ParamsMixin
from tm2p.anal.trends import Trends


class TopicDynamics(
    ParamsMixin,
):
    """:meta private:"""

    # ---------------------------------------------------------------------------
    def internal__compute_top_terms_by_year(self):
        self.terms_by_year = (
            Trends()
            .update(**self.params.__dict__)
            .update(terms_order_by="OCC")
            .update(term_counters=True)
            .run()
        )

    # ---------------------------------------------------------------------------
    def internal__compute_percentiles_per_term_by_year(self):

        year_q1 = []
        year_med = []
        year_q3 = []

        for _, row in self.terms_by_year.iterrows():
            sequence = []
            for item, year in zip(row, self.terms_by_year.columns):
                if item > 0:
                    sequence.extend([year] * int(item))

            year_q1.append(int(round(np.percentile(sequence, 25))))
            year_med.append(int(round(np.percentile(sequence, 50))))
            year_q3.append(int(round(np.percentile(sequence, 75))))

        self.terms_by_year["year_q1"] = year_q1
        self.terms_by_year["year_med"] = year_med
        self.terms_by_year["year_q3"] = year_q3

    # ---------------------------------------------------------------------------
    def internal__extract_total_occurrences_and_citations(self):

        self.terms_by_year = self.terms_by_year.assign(
            OCC=self.terms_by_year.index.map(
                lambda x: int(x.split(" ")[-1].split(":")[0])
            )
        )
        self.terms_by_year = self.terms_by_year.assign(
            global_citations=self.terms_by_year.index.map(
                lambda x: int(x.split(" ")[-1].split(":")[1])
            )
        )
        self.terms_by_year = self.terms_by_year[
            ["OCC", "global_citations", "year_q1", "year_med", "year_q3"]
        ]

        self.terms_by_year = self.terms_by_year.sort_values(
            by=["year_med", "OCC", "global_citations"],
            ascending=[True, False, False],
        )

    # ---------------------------------------------------------------------------
    def internal__select_top_terms_per_year(self):

        self.terms_by_year = self.terms_by_year.assign(
            rn=self.terms_by_year.groupby(["year_med"]).cumcount()
        ).sort_values(["year_med", "rn"], ascending=[True, True])

        self.terms_by_year = self.terms_by_year.query(
            f"rn < {self.params.items_per_year}"
        )

    # ---------------------------------------------------------------------------
    def internal__compute_bar_height_and_width(self):

        min_occ = self.terms_by_year.OCC.min()
        max_occ = self.terms_by_year.OCC.max()

        self.terms_by_year = self.terms_by_year.assign(
            height=0.15
            + 0.82 * (self.terms_by_year.OCC - min_occ) / (max_occ - min_occ)
        )

        self.terms_by_year = self.terms_by_year.assign(
            width=self.terms_by_year.year_q3 - self.terms_by_year.year_q1 + 1
        )

        self.terms_by_year = self.terms_by_year.sort_values(
            ["year_q1", "width", "height"], ascending=[True, True, True]
        )

    # ---------------------------------------------------------------------------
    def run(self):
        self.internal__compute_top_terms_by_year()
        self.internal__compute_percentiles_per_term_by_year()
        self.internal__extract_total_occurrences_and_citations()
        self.internal__select_top_terms_per_year()
        self.internal__compute_bar_height_and_width()
        return self.terms_by_year


#
