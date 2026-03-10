"""
Sort by Occurrences
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, SortByOccurrences

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the sorter
    >>> sorter = (
    ...     SortByOccurrences()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = StringIO()
    >>> print(output)  # doctest: +SKIP
    Sorting thesaurus by occurrences...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        FINTECH
          FINTECH; FINTECHS
        FINANCE
          FINANCE
        TECHNOLOGIES
          TECHNOLOGIES; TECHNOLOGY
        INNOVATION
          INNOVATION; INNOVATIONS
        FINANCIAL_SERVICE
          FINANCIAL_SERVICE; FINANCIAL_SERVICES
        FINANCIAL_TECHNOLOGIES
          FINANCIAL_TECHNOLOGIES; FINANCIAL_TECHNOLOGY
        BANKS
          BANKS
        THE_DEVELOPMENT
          THE_DEVELOPMENT; THE_DEVELOPMENTS
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByOccurrences as UserSortByOccurrences


class SortByOccurrences(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            UserSortByOccurrences()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .with_source_field("raw_descriptors")
            .run()
        )


# =============================================================================
