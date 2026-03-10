"""
Get Values
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
    >>> from tm2p.refine.thesaurus_old.descriptors import GetValues
    >>> terms = (
    ...     GetValues()
    ...     .with_patterns(["FINTECH", "FINANCIAL_TECHNOLOGIES"])
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    >>> terms[:5]
    ['FINANCIAL_TECHNOLOGIES', 'FINANCIAL_TECHNOLOGY', 'FINTECH', 'FINTECHS']




"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import GetValues as UserGetValues


#
#
class GetValues(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return (
            UserGetValues()
            .update(**self.params.__dict__)
            .with_thesaurus_file("concepts.the.txt")
            .run()
        )
