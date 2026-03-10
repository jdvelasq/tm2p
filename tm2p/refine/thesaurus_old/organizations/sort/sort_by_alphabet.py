"""
Sort by Alphabet
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, SortByAlphabet

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Create and run the sorter
    >>> sorter = (
    ...     SortByAlphabet()
    ...     .having_keys_ordered_by("alphabetical")
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

>>> from tm2p.refine.thesaurus_old.organizations import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()





"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByAlphabet as UserSortByAlphabet


class SortByAlphabet(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            UserSortByAlphabet()
            .update(**self.params.__dict__)
            .with_thesaurus_file("organizations.the.txt")
            .run()
        )
