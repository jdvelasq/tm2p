"""
Sort by Last Words
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByLastWords

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByLastWords()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by common last words...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      17 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        AGRICULTURE_PLAYS
          AGRICULTURE_PLAYS
        CHINA_EASTERN
          CHINA_EASTERN
        CONTINUANCE_INTENTION_DIFFERS
          CONTINUANCE_INTENTION_DIFFERS
        DIGITAL_FINANCE_ENCOMPASSES
          DIGITAL_FINANCE_ENCOMPASSES
        ENTREPRENEURIAL_ENDEAVOURS
          ENTREPRENEURIAL_ENDEAVOURS
        FOUR_SPECIFIC_INCREASES
          FOUR_SPECIFIC_INCREASES
        INNOVATIONS_EXACERBATE
          INNOVATIONS_EXACERBATE
        LENDINGCLUB_LOANS_INCREASES
          LENDINGCLUB_LOANS_INCREASES
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByLastWords as UserSortByLastWords


class SortByLastWords(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByLastWords()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
