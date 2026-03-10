"""
Sort by Word Length
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

    >>> from tm2p.refine.thesaurus_old.user import SortByWordLength
    >>> (
    ...     SortByWordLength()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_keys_ordered_by("alphabetical")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )




"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SortByWordLength(
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

        n_spaces = len(self.data_frame[self.data_frame["key"].str.contains(" ")])
        n_underscores = len(self.data_frame[self.data_frame["key"].str.contains("_")])

        if n_spaces > n_underscores:
            self.data_frame["length"] = self.data_frame["key"].str.split(" ")
        else:
            self.data_frame["length"] = self.data_frame["key"].str.split("_")
        self.data_frame["length"] = self.data_frame["length"].apply(
            lambda x: max(len(i) for i in x)
        )
        self.data_frame = self.data_frame.sort_values(
            ["length", "key"], ascending=[False, True]
        )

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
