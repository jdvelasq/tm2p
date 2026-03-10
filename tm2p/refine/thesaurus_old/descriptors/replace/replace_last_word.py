"""
Replace Last Word
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, ReplaceLastWord

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the replacer
    >>> replacer = (
    ...     ReplaceLastWord()
    ...     .having_word("FINTECH")
    ...     .having_replacement("fintech")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> replacer.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)  # doctest: +SKIP
    Replacing last word in keys...
             File : ...h/data/thesaurus/descriptors.the.txt
             Word : FINTECH
      Replacement : fintech
      9 replacements made successfully
      Replacement process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        ADOPTION_OF_fintech
          ADOPTION_OF_FINTECH
        AI_IN_fintech
          AI_IN_FINTECH
        CHARACTERIZE_fintech
          CHARACTERIZE_FINTECH
        EXPLORE_fintech
          EXPLORE_FINTECH
        fintech
          FINTECH; FINTECHS
        FRAME_fintech
          FRAME_FINTECH
        INTENTION_TO_ADOPT_fintech
          INTENTION_TO_ADOPT_FINTECH
        PROMPTPAY_fintech
          PROMPTPAY_FINTECH
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import ReplaceLastWord as UserReplaceEndsWithWord


class ReplaceLastWord(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserReplaceEndsWithWord()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# ===============================================================================
