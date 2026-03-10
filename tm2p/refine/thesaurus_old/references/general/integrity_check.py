"""
Integrity Check
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.references import IntegrityCheck

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Configure and run the integrity check
    >>> checker = (
    ...     IntegrityCheck()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> checker.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output) # doctest: +SKIP


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
            .with_thesaurus_file("references.the.txt")
            .with_source_field("global_references")
            .where_root_directory(self.params.root_directory)
            .run()
        )
