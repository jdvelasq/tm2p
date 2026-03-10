"""
Merge Keys
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()


    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()


    >>> from tm2p.refine.thesaurus_old.descriptors import MergeKeys
    >>> (
    ...     MergeKeys()
    ...     .with_patterns(["FINTECH", "FINANCIAL_TECHNOLOGIES"])
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Merging thesaurus keys...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      Keys : FINTECH; FINANCIAL_TECHNOLOGIES
      Merging process completed successfully
    <BLANKLINE>
    <BLANKLINE>

"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import MergeKeys as UserMergeKeys


class MergeKeys(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        (
            UserMergeKeys()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )


# =============================================================================
