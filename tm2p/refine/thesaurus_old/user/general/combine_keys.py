"""
Combine Keys
===============================================================================

Smoke tests:
    >>> from tm2p.refine.thesaurus_old.user import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 1721 keys found
      Header  :
        A_A_THEORY
          A_A_THEORY
        A_BASIC_RANDOM_SAMPLING_STRATEGY
          A_BASIC_RANDOM_SAMPLING_STRATEGY
        A_BEHAVIOURAL_PERSPECTIVE
          A_BEHAVIOURAL_PERSPECTIVE
        A_BETTER_UNDERSTANDING
          A_BETTER_UNDERSTANDING
        A_BLOCKCHAIN_IMPLEMENTATION_STUDY
          A_BLOCKCHAIN_IMPLEMENTATION_STUDY
        A_CASE_STUDY
          A_CASE_STUDY
        A_CHALLENGE
          A_CHALLENGE
        A_CLUSTER_ANALYSIS
          A_CLUSTER_ANALYSIS
    <BLANKLINE>

    >>> from tm2p.refine.thesaurus_old.user import ApplyThesaurus
    >>> (
    ...     ApplyThesaurus()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .with_other_field("descriptors_cleaned")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus applied successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 1788 keys applied
    <BLANKLINE>


    >>> from tm2p.refine.thesaurus_old.user import CombineKeys
    >>> df = (
    ...     CombineKeys()
    ...     #
    ...     # FIELD:
    ...     .with_field("descriptors_cleaned")
    ...     .having_items_in_top(100)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(5, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()
                       lead               candidate  probability combine?
    0       FINANCE 20:2992    TECHNOLOGIES 16:1847        0.550      yes
    1      SERVICES 07:1226      INVESTMENT 06:1294        0.571      yes
    2  PRACTITIONER 06:1194  BUSINESS_MODEL 05:1578        0.500      yes



"""

from tm2p._intern import ParamsMixin

# from tm2p.discov.co_occur_matrix._intern import (
#     DataFrame as CoocDataFrame,
# )


class CombineKeys(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def compute_cooc_matrix(self):

        self.cooc_matrix = (
            CoocDataFrame().update(**self.params.__dict__)
            #
            # ROWS:
            ## .with_other_field(None)
            ## .having_other_terms_in_top(None)
            ## .having_other_terms_ordered_by(None)
            ## .having_other_term_occurrences_between(None, None)
            ## .having_other_term_citations_between(None, None)
            ## .having_other_terms_in(None)
            #
            # COUNTERS:
            .using_counters(True)
            #
            .run()
        )

        self.cooc_matrix["rows_occ"] = self.cooc_matrix["rows"].apply(
            lambda x: int(x.split(" ")[1].split(":")[0]) if isinstance(x, str) else 0
        )

        self.cooc_matrix["rows_gc"] = self.cooc_matrix["rows"].apply(
            lambda x: int(x.split(" ")[1].split(":")[1]) if isinstance(x, str) else 0
        )

        self.cooc_matrix["columns_occ"] = self.cooc_matrix["columns"].apply(
            lambda x: int(x.split(" ")[1].split(":")[0]) if isinstance(x, str) else 0
        )

        self.cooc_matrix["columns_gc"] = self.cooc_matrix["columns"].apply(
            lambda x: int(x.split(" ")[1].split(":")[1]) if isinstance(x, str) else 0
        )

        self.cooc_matrix = self.cooc_matrix[
            self.cooc_matrix.rows_occ > self.cooc_matrix.columns_occ
        ]

        self.cooc_matrix

    # -------------------------------------------------------------------------
    def compute_probabilities(self):

        self.cooc_matrix["probability"] = (
            self.cooc_matrix.OCC / self.cooc_matrix.rows_occ
        )

        self.cooc_matrix["probability"] = self.cooc_matrix["probability"].round(3)

        self.cooc_matrix["combine?"] = self.cooc_matrix["probability"].apply(
            lambda x: "yes" if x >= 0.5 else "no"
        )

        self.cooc_matrix = self.cooc_matrix[self.cooc_matrix["combine?"] == "yes"]

        self.cooc_matrix = self.cooc_matrix.sort_values(
            by=["rows_occ", "rows_gc", "probability", "rows"], ascending=False
        )

        self.cooc_matrix = self.cooc_matrix.reset_index(drop=True)

    # -------------------------------------------------------------------------
    def format_final_output(self):

        # self.cooc_matrix["rows"] = self.cooc_matrix["rows"].apply(
        #     lambda x: x.split(" ")[0]
        # )
        # self.cooc_matrix["columns"] = self.cooc_matrix["columns"].apply(
        #     lambda x: x.split(" ")[0]
        # )
        self.cooc_matrix = self.cooc_matrix[
            ["rows", "columns", "probability", "combine?"]
        ]

        self.cooc_matrix.columns = ["lead", "candidate", "probability", "combine?"]

    # -------------------------------------------------------------------------
    def run(self):

        self.compute_cooc_matrix()
        self.compute_probabilities()
        self.format_final_output()
        return self.cooc_matrix
