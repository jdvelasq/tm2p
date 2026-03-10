"""
Replace Initial Word
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, ReplaceInitialWord

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the replacer
    >>> replacer = (
    ...     ReplaceInitialWord()
    ...     .having_word("FINTECH")
    ...     .having_replacement("fintech")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> replacer.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)  # doctest: +SKIP
    Replacing initial word in keys...
             File : ...h/data/thesaurus/descriptors.the.txt
             Word : FINTECH
      Replacement : fintech
      34 replacements made successfully
      Replacement process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        fintech
          FINTECH; FINTECHS
        fintech_AND_FINANCIAL_INNOVATIONS
          FINTECH_AND_FINANCIAL_INNOVATIONS
        fintech_AND_REGTECH
          FINTECH_AND_REGTECH
        fintech_BANKING_INDUSTRY
          FINTECH_BANKING_INDUSTRY
        fintech_BASED_INNOVATION_DEVELOPMENT
          FINTECH_BASED_INNOVATION_DEVELOPMENT
        fintech_BASED_INNOVATIONS
          FINTECH_BASED_INNOVATIONS; FINTECH_INNOVATION; FINTECH_INNOVATIONS
        fintech_CLUSTERS
          FINTECH_CLUSTERS
        fintech_COMPANIES
          FINTECH_COMPANIES
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import (
    ReplaceInitialWord as UserReplaceStartsWithWord,
)


class ReplaceInitialWord(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserReplaceStartsWithWord()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# ===============================================================================
