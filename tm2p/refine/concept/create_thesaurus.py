"""
CreateThesaurus
===============================================================================

Smoke tests:
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
      File         : ...fintech-with-references/refine/thesaurus/descriptors.the.txt
      Source field : DESCRIPTOR_TOK
      Status       : 2467 items added to the thesaurus.
    <BLANKLINE>


"""

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p.refine._intern.objs import ThesaurusCreationResult

from ..usr.create_thesaurus import CreateThesaurus as UserCreateThesaurus


class CreateThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> ThesaurusCreationResult:
        """:meta private:"""

        return (
            UserCreateThesaurus()
            .using_colored_output(self.params.colored_output)
            .with_source_field(Field.CONCEPT_RAW)
            .with_thesaurus_file("concepts.the.txt")
            .where_root_directory(self.params.root_directory)
            .run()
        )
