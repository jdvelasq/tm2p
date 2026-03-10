"""
Sort by Alphabet
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


    >>> from tm2p.refine.thesaurus_old.user import SortByAlphabet
    >>> (
    ...     SortByAlphabet()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_keys_ordered_by("alphabetical")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus sorted successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Header  :
        ABOUT_ONE_THIRD
          ABOUT_ONE_THIRD
        ACADEMIA
          ACADEMIA
        ACADEMICS
          ACADEMICS
        ACADEMIC_OBSERVERS
          ACADEMIC_OBSERVERS
        ACADEMIC_RESEARCH
          ACADEMIC_RESEARCH
        ACCELERATE_ACCESS
          ACCELERATE_ACCESS
        ACCEPTANCE_MODELS
          ACCEPTANCE_MODELS
        ACCESS
          ACCESS
    <BLANKLINE>




"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SortByAlphabet(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _prepare_data(self):
        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()

    # -------------------------------------------------------------------------
    def _sort_data(self):
        self.data_frame = self.data_frame.sort_values("key")

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
            status=None,
            data_frame=self.data_frame,
        )

    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusResult:

        self._prepare_data()
        self._sort_data()
        self._save_results()

        return self._create_result()


# =============================================================================
