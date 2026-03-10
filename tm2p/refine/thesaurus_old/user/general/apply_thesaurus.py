"""
Apply Thesaurus
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


    >>> from tm2p.io import Query
    >>> Query(
    ...     query_expression="SELECT descriptors_cleaned FROM database LIMIT 5;",
    ...     root_directory="examples/fintech/",
    ...     database="main",
    ...     record_years_range=(None, None),
    ...     record_citations_range=(None, None),
    ... ).run()  # doctest: +SKIP
                                     descriptors_cleaned
    0  AN_EFFECT; AN_INSTITUTIONAL_ASPECT; AN_MODERAT...
    1  ACTOR_NETWORK_THEORY; ANT; AN_UNPRECEDENTED_LE...
    2  AN_INITIAL_TECHNOLOGY_ADVANTAGE; CHINA; FINANC...
    3  AGGREGATION; ANALYSIS; AN_ADVANTAGE; AN_EXTENS...
    4  ACCESS; A_FORM; BEHAVIOURAL_ECONOMICS; DIGITAL...



    >>> from tm2p.ingest.oper import DeleteOperator
    >>> (
    ...     DeleteOperator()
    ...     .with_field("descriptors_cleaned")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import save_main_csv_zip
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class ApplyThesaurus(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__load_records(self) -> None:
        self.records = load_all_records_from_database(params=self.params)

    # -------------------------------------------------------------------------
    def internal__copy_field(self) -> None:
        if self.params.source_field != self.params.index_field:
            self.records[self.params.index_field] = self.records[
                self.params.source_field
            ].copy()

    # -------------------------------------------------------------------------
    def internal__split_other_field(self) -> None:
        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].str.split("; ")

    # -------------------------------------------------------------------------
    def internal__apply_thesaurus_to_other_field(self) -> None:

        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].map(
            lambda x: [self.mapping.get(item, item) for item in x],
            na_action="ignore",
        )

    # -------------------------------------------------------------------------
    def internal__remove_duplicates_from_other_field(self) -> None:
        #
        def f(x):
            # remove duplicated terms preserving the order
            terms = []
            for term in x:
                if term not in terms:
                    terms.append(term)
            return terms

        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].map(f, na_action="ignore")

    # -------------------------------------------------------------------------
    def internal__join_record_values(self) -> None:
        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].str.join("; ")

    # -------------------------------------------------------------------------
    def internal__write_records(self) -> None:
        save_main_csv_zip(params=self.params, records=self.records)

    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusResult:
        """:meta private:"""

        self._build_user_thesaurus_path()
        self.internal__load_reversed_thesaurus_as_mapping()
        self.internal__load_records()
        self.internal__copy_field()
        self.internal__split_other_field()
        self.internal__apply_thesaurus_to_other_field()
        self.internal__remove_duplicates_from_other_field()
        self.internal__join_record_values()
        self.internal__write_records()

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus applied successfully.",
            success=True,
            status=f"{len(self.mapping.keys())} keys applied",
            data_frame=None,
        )


# =============================================================================
