"""
Sort by StartsWith Match
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

    >>> from tm2p.refine.thesaurus_old.user import SortByStartsWithMatch
    >>> (
    ...     SortByStartsWithMatch()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_text_matching("BUSINESS")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus sorted successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 7 matches found
      Header  :
        BUSINESS
          BUSINESS; BUSINESSES
        BUSINESS_DEVELOPMENT
          BUSINESS_DEVELOPMENT
        BUSINESS_INFRASTRUCTURE
          BUSINESS_INFRASTRUCTURE; BUSINESS_INFRASTRUCTURES
        BUSINESS_MODEL
          BUSINESS_MODEL; BUSINESS_MODELS
        BUSINESS_OPPORTUNITIES
          BUSINESS_OPPORTUNITIES
        BUSINESS_PROCESS
          BUSINESS_PROCESS
        BUSINESS_TO_CONSUMERS_MODELS
          BUSINESS_TO_CONSUMERS_MODELS
        A_A_THEORY
          A_A_THEORY
    <BLANKLINE>




"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SortByStartsWithMatch(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.n_matches: int = 0

    # -------------------------------------------------------------------------
    def _prepare_data(self):
        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()

    # -------------------------------------------------------------------------
    def _sort_data(self):
        self._select_data_frame_rows()
        self._sort_data_frame_by_rows_and_key()

    # -------------------------------------------------------------------------
    def _select_data_frame_rows(self):
        #
        self.data_frame["__row_selected__"] = False
        #

        #
        if isinstance(self.params.pattern, str):
            self.params.pattern = [self.params.pattern]

        for pat in self.params.pattern:

            self.data_frame.loc[
                self.data_frame.key.str.startswith(pat=pat),
                "__row_selected__",
            ] = True

        self.n_matches = self.data_frame.__row_selected__.sum()

    # -------------------------------------------------------------------------
    def _save_results(self):
        self._write_thesaurus_data_frame_to_disk()

    # -------------------------------------------------------------------------
    def _create_result(self) -> ThesaurusResult:

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus sorted successfully.",
            success=True,
            status=f"{self.n_matches} matches found",
            data_frame=self.data_frame,
        )

    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusResult:

        self._prepare_data()
        self._sort_data()
        self._save_results()

        return self._create_result()


# =============================================================================
