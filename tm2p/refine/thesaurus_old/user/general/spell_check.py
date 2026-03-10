"""
Spell Check
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


    >>> from tm2p.refine.thesaurus_old.user import SpellCheck
    >>> (
    ...     SpellCheck()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_maximum_occurrence(3)
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus keys reduced successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 82 misspelled keys found.
      Header  :
        A_BEHAVIOURAL_PERSPECTIVE
          A_BEHAVIOURAL_PERSPECTIVE
        A_BLOCKCHAIN_IMPLEMENTATION_STUDY
          A_BLOCKCHAIN_IMPLEMENTATION_STUDY
        A_HYBRID_MCDM_MODEL
          A_HYBRID_MCDM_MODEL
        A_MULTI_LEVEL_ANALYSIS
          A_MULTI_LEVEL_ANALYSIS
        A_WIDE_RANGING_RECONCEPTUALIZATION
          A_WIDE_RANGING_RECONCEPTUALIZATION
        A_YOUTH_MICROLOAN_STARTUP
          A_YOUTH_MICROLOAN_STARTUP
        AFFORDANCE_ACTUALIZATION
          AFFORDANCE_ACTUALIZATION
        AGROINDUSTRY
          AGROINDUSTRY
    <BLANKLINE>



"""

import pandas as pd  # type: ignore
from spellchecker import SpellChecker as ExternalSpellChecker

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SpellCheck(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.words: list[str] = []
        self.misspelled_words: list[str] = []
        self.misspelled_keys: int = 0

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__extract_words_from_mapping(self) -> None:

        terms = list(self.mapping.keys())
        terms = [t.replace("_", " ") for t in terms]
        tokens = [word for term in terms for word in term.split(" ")]
        counts = pd.Series(tokens).value_counts()
        counts = counts[counts <= self.params.maximum_occurrence]
        words = [word for word in counts.index if word.isalpha()]
        self.words = words

    # -------------------------------------------------------------------------
    def internal__search_mispelled_words(self) -> None:

        spell = ExternalSpellChecker()
        misspelled_set = spell.unknown(self.words)
        self.misspelled_words = sorted(misspelled_set)

    # -------------------------------------------------------------------------
    def internal__select_data_frame_rows(self) -> None:

        self.data_frame["__row_selected__"] = False

        self.data_frame["fingerprint"] = self.data_frame["key"].copy()
        self.data_frame["fingerprint"] = (
            self.data_frame["fingerprint"]
            .str.lower()
            .str.replace("_", " ")
            .str.split(" ")
        )

        for word in self.misspelled_words:
            self.data_frame.loc[
                self.data_frame.fingerprint.str.contains(word, regex=False),
                "__row_selected__",
            ] = True

        self.misspelled_keys = self.data_frame.__row_selected__.sum()

    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusResult:
        """:meta private:"""

        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__extract_words_from_mapping()
        self.internal__search_mispelled_words()
        self.internal__select_data_frame_rows()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus keys reduced successfully.",
            success=True,
            status=f"{self.misspelled_keys} misspelled keys found.",
            data_frame=self.data_frame,
        )


# =============================================================================
