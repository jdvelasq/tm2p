"""
Sort by Last Word
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


    >>> from tm2p.refine.thesaurus_old.user import SortByLastWords
    >>> (
    ...     SortByLastWords()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus sorted successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 17 matches found
      Header  :
        AGRICULTURE_PLAYS
          AGRICULTURE_PLAYS
        CHINA_EASTERN
          CHINA_EASTERN
        CONTINUANCE_INTENTION_DIFFERS
          CONTINUANCE_INTENTION_DIFFERS
        DIGITAL_FINANCE_ENCOMPASSES
          DIGITAL_FINANCE_ENCOMPASSES
        ENTREPRENEURIAL_ENDEAVOURS
          ENTREPRENEURIAL_ENDEAVOURS
        FOUR_SPECIFIC_INCREASES
          FOUR_SPECIFIC_INCREASES
        INNOVATIONS_EXACERBATE
          INNOVATIONS_EXACERBATE
        LENDINGCLUB_LOANS_INCREASES
          LENDINGCLUB_LOANS_INCREASES
    <BLANKLINE>




"""

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SortByLastWords(
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
    def _select_data_frame_rows(self) -> None:

        self.data_frame["__row_selected__"] = False

        patterns = load_builtin_word_list("common_last_words.txt")
        patterns = [pattern.strip().upper() for pattern in patterns]

        for pattern in patterns:

            self.data_frame.loc[
                self.data_frame.key.str.endswith(pat="_" + pattern),
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
