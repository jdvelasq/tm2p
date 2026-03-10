"""
Integrity Check
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, IntegrityCheck

    >>> # Redirect stderr to capture output
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True, ).run()

    >>> # Run the integrity check
    >>> checker = (
    ...     IntegrityCheck()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> checker.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Checking thesaurus integrity...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      1788 terms checked
      Integrity check completed successfully
    <BLANKLINE>
    <BLANKLINE>


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
            .with_thesaurus_file("concepts.the.txt")
            .with_source_field("raw_descriptors")
            .where_root_directory(self.params.root_directory)
            .run()
        )
