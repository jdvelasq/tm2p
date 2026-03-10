"""
MergeKeys
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.countries import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/tests/refine/thesaurus/countries.the.txt
      Source field : COUNTRY_AND_AFFIL
      Status       : 21 countries added to the thesaurus.
    <BLANKLINE>




    >>> from tm2p.refine.countries import MergeKeys
    >>> (
    ...     MergeKeys()
    ...     .having_preferred_key("China")
    ...     .having_variant_keys(("Hong Kong",))
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )



"""

from tm2p import Field, ThesaurusField
from tm2p._intern import ParamsMixin

from ..usr.merge_keys import MergeKeys as UserMergeKeys

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

        return (
            UserMergeKeys()
            .update(**self.params.__dict__)
            .with_thesaurus_file("countries.the.txt")
            .with_source_field(Field.CTRY_AFFIL)
            .run()
        )
