"""
Sort by Fuzzy Match
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByFuzzyMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByFuzzyMatch()
    ...     .having_text_matching("INFORM")
    ...     .using_match_threshold(50)
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output) # doctest: +SKIP
    Sorting thesaurus by fuzzy match...
                File : examples/fintech/data/thesaurus/descriptors.the.txt
           Keys like : INFORM
      Match thresold : 50
      81 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        A_DISINTERMEDIATION_FORCE
          A_DISINTERMEDIATION_FORCE
        A_FIRM
          A_FIRM
        A_FORM
          A_FORM
        A_NEW_INTERMEDIARY
          A_NEW_INTERMEDIARY
        A_PLATFORM
          A_PLATFORM
        BUSINESS_INFRASTRUCTURES
          BUSINESS_INFRASTRUCTURES
        BUT_THE_FINANCIAL_REGULATORY_REFORMS
          BUT_THE_FINANCIAL_REGULATORY_REFORMS
        CHANGE_FINANCIAL_INTERMEDIATION_STRUCTURES
          CHANGE_FINANCIAL_INTERMEDIATION_STRUCTURES
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByFuzzyMatch as UserSortByFuzzyMatch


class SortByFuzzyMatch(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByFuzzyMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
