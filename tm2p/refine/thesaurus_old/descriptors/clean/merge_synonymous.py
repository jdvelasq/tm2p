"""
Merge Synonymous
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, MergeSynonymous

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Merge synonymous terms
    >>> (
    ...     MergeSynonymous()
    ...     .with_core_area("FINTECH - FINANCIAL TECHNOLOGIES")
    ...     .having_n_contexts(10)
    ...     .having_items_in_top(40)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)  # doctest: +SKIP



"""

import json
import os

import pandas as pd
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin

# from tm2p._intern.stopwords import load_user_stopwords, save_user_stopwords

# -----------------------------------------------------------------------------


class MergeSynonymous(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        from tm2p.refine.thesaurus_old.descriptors import AreSynonymous, MergeKeys

        df = AreSynonymous().update(**self.params.__dict__).run()

        for _, row in df.iterrows():

            if row["candidate_terms"].strip() != "":

                for candidate_term in row["candidate_terms"].split("; "):
                    self.params.with_patterns([row.lead_term, candidate_term])
                    MergeKeys().update(**self.params.__dict__).run()


# =============================================================================
