"""
Integrity Check
===============================================================================

Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


    >>> from tm2p.refine.thesaurus_old.countries import IntegrityCheck
    >>> (
    ...     IntegrityCheck()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import IntegrityCheck as UserIntegrityCheck


class IntegrityCheck(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        (
            UserIntegrityCheck()
            .update(**self.params.__dict__)
            .update(
                thesaurus_file="countries.the.txt",
                field="affiliations",
                root_directory=self.params.root_directory,
            )
            .run()
        )


# =============================================================================
