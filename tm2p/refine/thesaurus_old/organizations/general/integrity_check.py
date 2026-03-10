"""
Integrity Check
===============================================================================

Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, IntegrityCheck

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> checker = (
    ...     IntegrityCheck()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> checker.run()




"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import IntegrityCheck as UserIntegrityCheck


#
#
class IntegrityCheck(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        (
            UserIntegrityCheck()
            .update(**self.params.__dict__)
            .with_thesaurus_file("organizations.the.txt")
            .with_source_field("affiliations")
            .where_root_directory(self.params.root_directory)
            .run()
        )
