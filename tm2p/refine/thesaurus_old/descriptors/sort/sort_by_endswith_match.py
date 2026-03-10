"""
Sort By EndsWith Match
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByEndsWithMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByEndsWithMatch()
    ...     .having_text_matching("BANKS")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by endswith match...
         File : examples/fintech/data/thesaurus/descriptors.the.txt
      Pattern : BANKS
      13 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        BANKS
          BANKS
        CITY_COMMERCIAL_BANKS
          CITY_COMMERCIAL_BANKS
        COMMERCIAL_BANKS
          COMMERCIAL_BANKS
        ENABLE_BANKS
          ENABLE_BANKS
        FIVE_MAJOR_COMMERCIAL_BANKS
          FIVE_MAJOR_COMMERCIAL_BANKS
        INCUMBENT_RETAIL_BANKS
          INCUMBENT_RETAIL_BANKS
        LEADING_EUROPEAN_AND_US_BANKS
          LEADING_EUROPEAN_AND_US_BANKS
        NOWADAYS_BANKS
          NOWADAYS_BANKS
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import (
    SortByEndsWithMatch as UserSortByEndsWithMatch,
)


class SortByEndsWithMatch(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByEndsWithMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
