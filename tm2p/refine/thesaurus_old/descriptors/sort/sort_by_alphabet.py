"""
Sort by Alphabet
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByAlphabet

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByAlphabet()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = StringIO()
    >>> print(output) # doctest: +SKIP
    Sorting thesaurus alphabetically...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        ABOUT_ONE_THIRD
          ABOUT_ONE_THIRD
        ACADEMIA
          ACADEMIA
        ACADEMICS
          ACADEMICS
        ACADEMIC_OBSERVERS
          ACADEMIC_OBSERVERS
        ACADEMIC_RESEARCH
          ACADEMIC_RESEARCH
        ACCELERATE_ACCESS
          ACCELERATE_ACCESS
        ACCESS
          ACCESS
        ACCESS_LOANS
          ACCESS_LOANS
    <BLANKLINE>
    <BLANKLINE>




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
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
