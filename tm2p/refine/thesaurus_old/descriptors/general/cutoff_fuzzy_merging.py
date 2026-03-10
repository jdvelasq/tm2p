"""
Cutoff Fuzzy Merging
===============================================================================


Smoke tests:
    >>> # Reset the thesaurus to initial state
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> from tm2p.refine.thesaurus_old.descriptors import ReduceKeys
    >>> (
    ...     ReduceKeys()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )


    >>> # Redirect stderr to capture output
    >>> import sys
    >>> from io import StringIO
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Cutoff Fuzzy Merging
    >>> from tm2p.refine.thesaurus_old.descriptors import CutoffFuzzyMerging
    >>> (
    ...     CutoffFuzzyMerging(tqdm_disable=True, )
    ...     # .where_root_directory("examples/fintech/")
    ...     .where_root_directory("../tm2_economics_of_wind_energy/")
    ...     .using_cutoff_threshold(85)
    ...     .using_match_threshold(95)
    ...     .run()
    ... )

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output) # doctest: +SKIP
    Cutoff-Fuzzy Merging thesaurus keys...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      Keys reduced from 1569 to 1554
      Merging process completed successfully
    <BLANKLINE>
    <BLANKLINE>





"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import CutoffFuzzyMerging as UserCutoffFuzzyMerging


#
#
class CutoffFuzzyMerging(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        (
            UserCutoffFuzzyMerging()
            .update(**self.params.__dict__)
            .update(
                field="raw_descriptors",
                thesaurus_file="concepts.the.txt",
                root_directory=self.params.root_directory,
                tqdm_disable=self.params.tqdm_disable,
                cutoff_threshold=self.params.similarity_cutoff,
                match_threshold=self.params.fuzzy_threshold,
                quiet=self.params.quiet,
            )
            .run()
        )
