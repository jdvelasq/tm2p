"""
Get Contexts
===============================================================================


Smoke tests:
    >>> # Redirecting stderr to avoid messages during doctests
    >>> import sys
    >>> from io import StringIO
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Reset the thesaurus to initial state
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus
    >>> InitializeThesaurus(
    ...     root_directory="examples/fintech/",
    ...     quiet=True,
    ... ).run()

    >>> # Creates, configures, an run the exploder
    >>> from tm2p.refine.thesaurus_old.descriptors import GetContexts
    >>> contexts = (
    ...     GetContexts()
    ...     .with_patterns(["FINTECH"])
    ...     .having_n_contexts(10)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    >>> from pprint import pprint
    >>> pprint(contexts[:5])
    ['- this research represents a stepping stone in exploring the interaction '
     'between fintech and its yet unfolding social and political context .',
     '- it also discusses policy implications for china fintech industry , '
     'focusing on the changing role of the state in fostering the growth of '
     'national industry within and outside of china .',
     '- financial technologies ( fintech ) have become an integral part of banking '
     ', and nowadays banks have started to compete beyond financial services '
     'facing increasing competition from nonfinancial institutions providing , for '
     'example , payment services .',
     '- the rapid rise of fintech has changed the business landscape in banking '
     'asking for more innovative solutions .',
     '- these recent tendencies require the banks to increase investment in '
     'fintech , rethink service distribution channels , especially the business to '
     'consumers models , increase further standardization of backoffice functions '
     ', etc .']






"""

import sys

from tm2p._intern import ParamsMixin
from tm2p.discov.concord import SentenceConcordance


class GetContexts(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        from tm2p.refine.thesaurus_old.descriptors import GetValues

        if self.params.quiet is False:
            sys.stderr.write("Getting contexts...\n")
            sys.stderr.flush()

        terms = GetValues(quiet=self.params.quiet).update(**self.params.__dict__).run()

        complete_contexts = []

        for term in terms:

            contexts = (
                SentenceConcordance()
                .update(**self.params.__dict__)
                .having_text_matching(term)
                .run()
            )

            contexts = [c for c in contexts if len(c) > 80]
            contexts = [f"- {c} ." for c in contexts]
            contexts = [c.lower().replace("_", " ") for c in contexts]

            complete_contexts.extend(contexts)

        patterns = [
            pattern.lower().replace("_", " ") for pattern in self.params.pattern
        ]
        complete_contexts = [
            c for c in complete_contexts if any(pattern in c for pattern in patterns)
        ]

        if self.params.quiet is False:
            sys.stderr.write("Getting contexts completed successfully\n")
            sys.stderr.flush()

        return complete_contexts[: self.params.n_contexts]
