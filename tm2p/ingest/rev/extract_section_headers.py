"""
ExtractSectionHeaders
===============================================================================

Smoke test:
    >>> from tm2p.ingest.rev import ExtractSectionHeaders
    >>> text = (
    ...     ExtractSectionHeaders()
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    >>> assert isinstance(text, list)
    >>> assert all(isinstance(t, str) for t in text)
    >>> for t in text[:5]: print(t)
                                                         purpose  :  this_study_aims_to_examine_the_relationship_between the D…
                                 design / methodology / approach  :  AN_EXTENSIVE_REVIEW of THE_LITERATURE was carried out , a…
                                                        findings  :  the_findings of the empirical results_indicate_that_there…
                                          practical implications  :  this_study , hence , recommends that POLICYMAKERS and GOV…
                                             originality / value  :  this_paper_offers NEW_CONTRIBUTIONS to THE_GCC_LITERATURE…


"""

from tm2p._intern import ParamsMixin
from tm2p.discov.concord import ConcordanceUppercase

__reviewed__ = "2026-01-28"


class ExtractSectionHeaders(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> list[str]:

        return (
            ConcordanceUppercase()
            .update(**self.params.__dict__)
            .having_text_matching(" : ")
            .run()
        )
