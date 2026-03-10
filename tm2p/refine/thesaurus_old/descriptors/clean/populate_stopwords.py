"""
Populate Stopwords
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, PopulateStopwords

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Populate stopwords
    >>> (
    ...     PopulateStopwords()
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

from tm2p._intern import ParamsMixin

# from tm2p._intern.stopwords import load_user_stopwords, save_user_stopwords
from tm2p.refine.thesaurus_old.descriptors import IsStopword

# -----------------------------------------------------------------------------


class PopulateStopwords(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = IsStopword().update(**self.params.__dict__).run()
        new_stopwords = df[df["is_stopword?"]]["descriptor"].tolist()
        stopwords = load_user_stopwords(params=self.params)
        stopwords = sorted(set(stopwords).union(set(new_stopwords)))
        save_user_stopwords(self.params, stopwords)
