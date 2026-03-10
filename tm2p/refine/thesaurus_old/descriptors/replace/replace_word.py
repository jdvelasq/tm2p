"""
Replace Word
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, ReplaceWord

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the replacer
    >>> replacer = (
    ...     ReplaceWord()
    ...     .having_word("FINTECH")
    ...     .having_replacement("fintech")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> replacer.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output) # doctest: +SKIP
    Replacing word in keys...
             File : ...h/data/thesaurus/descriptors.the.txt
             Word : FINTECH
      Replacement : fintech
      93 replacements made successfully
      Replacement process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        A_EUROPEAN_OR_NATIONAL_fintech_MARKET
          A_EUROPEAN_OR_NATIONAL_FINTECH_MARKET
        A_fintech_COMPANY
          A_FINTECH_COMPANY
        A_fintech_ECOSYSTEM
          A_FINTECH_ECOSYSTEM
        A_NEW_fintech_INNOVATION_MAPPING_APPROACH
          A_NEW_FINTECH_INNOVATION_MAPPING_APPROACH
        A_THEORETICAL_DATA_DRIVEN_fintech_FRAMEWORK
          A_THEORETICAL_DATA_DRIVEN_FINTECH_FRAMEWORK
        ACTIVE_fintech_SOLUTIONS
          ACTIVE_FINTECH_SOLUTIONS
        ADOPTION_OF_fintech
          ADOPTION_OF_FINTECH
        ADOPTION_OF_fintech_SERVICES
          ADOPTION_OF_FINTECH_SERVICES
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import ReplaceWord as UserReplaceWord


class ReplaceWord(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserReplaceWord()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# ===============================================================================
