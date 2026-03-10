"""
FuzzyCutoff1Match
===============================================================================

Smoke test:
    >>> from tm2p import Field

    >>> from tm2p.refine.descriptors import CreateThesaurus

    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/tests/refine/thesaurus/descriptors.the.txt
      Source field : CONCEPT_RAW
      Status       : 2441 items added to the thesaurus.
    <BLANKLINE>


    >>> from tm2p.refine.descriptors.pre_process_thesaurus import PreProcessThesaurus
    >>> (
    ...     PreProcessThesaurus()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Fuzzy cutoff matching completed.
      Success        : True
      Field          : _UNSPECIFIED_
      Thesaurus      : descriptors.the.txt
    <BLANKLINE>


    >>> from tm2p.refine.descriptors.fuzzy_cutoff_1_word_match import FuzzyCutoffOneWordMatch
    >>> (
    ...     FuzzyCutoffOneWordMatch()
    ...     .using_colored_output(False)
    ...     .using_similarity_cutoff(88)
    ...     .using_fuzzy_threshold(80)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Fuzzy cutoff 1-word matching completed.
      Success        : True
      Field          : _UNSPECIFIED_
      Thesaurus      : descriptors.the.txt
    <BLANKLINE>


"""

import sys

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p.refine._intern.objs.thesaurus_match_result import ThesaurusMatchResult
from tm2p.refine._intern.rule import apply_fuzzy_cutoff_1_word_rule

from .._intern.data_access import load_thesaurus_as_dataframe


class FuzzyCutoffOneWordMatch(
    ParamsMixin,
):
    """:meta private:"""

    _HEADER_WIDTH = 70
    _STEP_PREFIX = "  → "

    def _write(self, text: str) -> None:
        sys.stderr.write(text)
        sys.stderr.flush()

    def _print_header(self) -> None:
        separator = "=" * self._HEADER_WIDTH
        self._write(f"\n{separator}\nFuzzy Cutoff 1-word Matching\n{separator}\n\n")

    def run(self) -> ThesaurusMatchResult:

        self.with_thesaurus_file("concepts.the.txt")
        self.with_source_field(Field.CONCEPT_RAW)

        thesaurus_df = load_thesaurus_as_dataframe(params=self.params)

        self._print_header()
        self._write(f"{self._STEP_PREFIX}Applying fuzzy cutoff 1-word rule\n")

        apply_fuzzy_cutoff_1_word_rule(
            thesaurus_df=thesaurus_df,
            params=self.params,
        )

        return ThesaurusMatchResult(
            colored_output=self.params.colored_output,
            output_file=None,
            thesaurus_file=self.params.thesaurus_file,
            msg="Fuzzy cutoff 1-word matching completed.",
            success=True,
            field=self.params.source_field.value,
        )
