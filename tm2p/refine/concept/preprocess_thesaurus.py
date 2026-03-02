"""
PreProcessThesaurus
===============================================================================

Smoke test:
    >>> from tm2p import Field

    >>> from tm2p.refine.descriptors import CreateThesaurus

    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/tests/refine/thesaurus/descriptors.the.txt
      Source field : DESCRIPTOR_TOK
      Status       : 2441 items added to the thesaurus.
    <BLANKLINE>

    >>> from tm2p.refine.descriptors.pre_process_thesaurus import PreProcessThesaurus
    >>> (
    ...     PreProcessThesaurus()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    INFO: Fuzzy cutoff matching completed.
      Success        : True
      Field          : _UNSPECIFIED_
      Thesaurus      : descriptors.the.txt
    <BLANKLINE>


"""

import sys

from tm2p import Field, ThesaurusField
from tm2p._intern import ParamsMixin
from tm2p.refine._intern.objs.thesaurus_match_result import ThesaurusMatchResult
from tm2p.refine._intern.rule import (
    apply_chemical_compounds_rule,
    apply_common_and_basic_rule,
    apply_error_metrics_rule,
    apply_exact_match_rule,
    apply_geographic_names_rule,
    apply_hyphenation_rule,
    apply_inflected_verb_forms_rule,
    apply_leading_noise_removal_rule,
    apply_num_punct_to_space_rule,
    apply_number_to_letter_rule,
    apply_plural_singular_rule,
    apply_prefer_singular_over_plural_rule,
    apply_punctuation_variation_rule,
    apply_scientific_and_academic_rule,
    apply_trailing_noise_removal_rule,
    apply_white_space_normalization_rule,
    apply_xml_encoding_rule,
)

from .._intern.data_access import (
    load_thesaurus_as_dataframe,
    save_dataframe_as_thesaurus,
)

PREFERRED = ThesaurusField.PREFERRED.value


class PreProcessThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    _HEADER_WIDTH = 70
    _STEP_PREFIX = "  → Rule : "
    _ORDINAL = ["First", "Second"]

    def _write(self, text: str) -> None:
        sys.stderr.write(text)
        sys.stderr.flush()

    def _print_header(self) -> None:
        separator = "=" * self._HEADER_WIDTH
        self._write(f"\n{separator}\nPre-processing Thesaurus\n{separator}\n")

    def run(self) -> ThesaurusMatchResult:

        self.with_thesaurus_file("concepts.the.txt")
        self.with_source_field(Field.CONCEPT_RAW)

        thesaurus_df = load_thesaurus_as_dataframe(params=self.params)

        self._print_header()

        for phase in range(2):

            self._write(f"\n[{phase+1}] {self._ORDINAL[phase]} Pass\n")

            for msg, rule in [
                ("exact match", apply_exact_match_rule),
                ("geographic names", apply_geographic_names_rule),
                ("error metrics", apply_error_metrics_rule),
                ("number to letter", apply_number_to_letter_rule),
                ("num punct to space", apply_num_punct_to_space_rule),
                ("xml encoding", apply_xml_encoding_rule),
                ("white space normalization", apply_white_space_normalization_rule),
                ("chemical compounds", apply_chemical_compounds_rule),
                ("punctuation variation", apply_punctuation_variation_rule),
                ("hyphenation", apply_hyphenation_rule),
                ("plural singular", apply_plural_singular_rule),
                ("prefer singular over plural", apply_prefer_singular_over_plural_rule),
                ("common and basic", apply_common_and_basic_rule),
                ("scientific and academic", apply_scientific_and_academic_rule),
                ("inflected verb forms", apply_inflected_verb_forms_rule),
                ("leading noise removal", apply_leading_noise_removal_rule),
                ("trailing noise removal", apply_trailing_noise_removal_rule),
            ]:
                self._write(f"{self._STEP_PREFIX}{msg}\n")
                thesaurus_df = rule(thesaurus_df, self.params)

        thesaurus_df = thesaurus_df.sort_values(by=[PREFERRED])
        save_dataframe_as_thesaurus(params=self.params, dataframe=thesaurus_df)

        return ThesaurusMatchResult(
            colored_output=self.params.colored_output,
            output_file=None,
            thesaurus_file=self.params.thesaurus_file,
            msg="Fuzzy cutoff matching completed.",
            success=True,
            field=self.params.source_field.value,
        )
