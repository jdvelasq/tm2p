"""
Merge Keys
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.user import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .with_source_field(Field.DESCRIPTOR_TOK)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/tests/refine/thesaurus/demo.the.txt
      Source field : DESCRIPTOR_TOK
      Status       : 2441 items added to the thesaurus.
    <BLANKLINE>


    >>> from tm2p.refine.user import MergeKeys
    >>> (
    ...     MergeKeys()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_preferred_key("fintech")
    ...     .having_variant_keys(("financial technology", "financial technologies"))
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )



"""

from tm2p import ThesaurusField
from tm2p._intern import ParamsMixin

from .._intern.data_access import (
    load_thesaurus_as_dataframe,
    save_dataframe_as_thesaurus,
)

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
SIGNATURE = ThesaurusField.SIGNATURE.value
VARIANT = ThesaurusField.VARIANT.value


class MergeKeys(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        # self.with_thesaurus_file("concepts.the.txt")
        # self.with_source_field(Field.DESCRIPTOR_TOK)

        preferred = self.params.preferred_key
        variants = self.params.variant_keys

        thesaurus_df = load_thesaurus_as_dataframe(params=self.params)

        thesaurus_df[OLD] = thesaurus_df[PREFERRED]
        thesaurus_df[VARIANT] = thesaurus_df[VARIANT].str.split("; ")
        thesaurus_df = thesaurus_df.explode(VARIANT)
        thesaurus_df[PREFERRED] = thesaurus_df[PREFERRED].apply(
            lambda x: preferred if x in variants else x
        )
        thesaurus_df[CHANGED] = thesaurus_df[PREFERRED] != thesaurus_df[OLD]

        groupby_df = thesaurus_df.groupby(PREFERRED, as_index=False).agg(
            {
                VARIANT: lambda x: "; ".join(sorted(set(x))),
                CHANGED: any,
            }
        )
        groupby_df = groupby_df.sort_values(
            [CHANGED, PREFERRED], ascending=[False, True]
        )

        save_dataframe_as_thesaurus(params=self.params, dataframe=groupby_df)
