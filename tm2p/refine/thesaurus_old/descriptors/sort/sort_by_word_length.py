"""
Sort by Word Length
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByWordLength

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByWordLength()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)  # doctest: +SKIP
    Sorting thesaurus by word length...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        COMPETITION (ECONOMICS)
          COMPETITION (ECONOMICS)
        FINANCIAL_TECHNOLOGY (FINTECH)
          FINANCIAL_TECHNOLOGY (FINTECH)
        A_WIDE_RANGING_RECONCEPTUALIZATION
          A_WIDE_RANGING_RECONCEPTUALIZATION
        NETWORKS (CIRCUITS)
          NETWORKS (CIRCUITS)
        THE_RECONCEPTUALIZATION
          THE_RECONCEPTUALIZATION
        CLASSIFICATION (OF_INFORMATION)
          CLASSIFICATION (OF_INFORMATION)
        EXPLORE_INTERRELATIONSHIPS
          EXPLORE_INTERRELATIONSHIPS
        A_DISINTERMEDIATION_FORCE
          A_DISINTERMEDIATION_FORCE
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByWordLength as UserSortByWordLength


class SortByWordLength(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByWordLength()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
