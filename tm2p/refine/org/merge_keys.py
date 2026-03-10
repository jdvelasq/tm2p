"""
MergeKeys
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.organizations import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/tests/refine/thesaurus/organizations.the.txt
      Source field : ORGANIZATION_AND_AFFIL
      Status       : 45 organizations added to the thesaurus.
    <BLANKLINE>




    >>> from tm2p.refine.organizations import MergeKeys
    >>> (
    ...     MergeKeys()
    ...     .having_preferred_key("Addis Ababa University [ETH]")
    ...     .having_variant_keys(("Agricultural Bank of China [CHN]",))
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
            .with_thesaurus_file("organizations.the.txt")
            .with_source_field(Field.ORG_AFFIL)
            .run()
        )
