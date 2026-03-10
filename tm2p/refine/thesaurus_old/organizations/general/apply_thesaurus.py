"""
Apply Thesaurus
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import ApplyThesaurus, InitializeThesaurus

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()


    >>> (
    ...     ApplyThesaurus()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     #
    ...     .run()
    ... )


    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/organizations.the.txt
      Source field : affiliations
      Target field : organizations
      Application process completed successfully
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import internal__transform
from tm2p.refine.thesaurus_old.user import ApplyThesaurus as ApplyUserThesaurus


#
#
class ApplyThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        # Affiliations to countries mmapping
        (
            ApplyUserThesaurus(quiet=self.params.quiet)
            .update(**self.params.__dict__)
            .with_thesaurus_file("organizations.the.txt")
            .with_source_field("affiliations")
            .with_other_field("organizations")
            .where_root_directory(self.params.root_directory)
            .run()
        )

        # Country of first author
        internal__transform(
            #
            # FIELD:
            field="organizations",
            other_field="organization_1st_author",
            function=lambda x: x.str.split("; ").str[0],
            root_dir=self.params.root_directory,
        )
