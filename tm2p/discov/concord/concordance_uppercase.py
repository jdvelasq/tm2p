"""
Concordance Uppercase
=========================================================================================

Smoke test:
    >>> from tm2p import RecordsOrderBy
    >>> from tm2p.analyze.concordances import ConcordanceUppercase
    >>> contexts = (
    ...     ConcordanceUppercase()
    ...     #
    ...     # PATTERN:
    ...     .having_text_matching("FINTECH")
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordsOrderBy.PUBYEAR_NEWEST)
    ...     #
    ...     .run()
    ... )
    >>> assert isinstance(contexts, list)
    >>> assert len(contexts) > 0
    >>> assert all(isinstance(c, str) for c in contexts)
    >>> for t in contexts[:10]: print(t) # doctest: +SKIP
                           this_paper_explores THE_COMPLEXITY of FINTECH , and attempts A_DEFINITION , drawn from A_PROCESS of rev…
      …NITION concentrates on extracting out THE_QUINTESSENCE of FINTECH using BOTH_SPHERES
      …erreviewed DEFINITIONS of THE_TERM , it_is_concluded_that FINTECH is A_NEW_FINANCIAL_INDUSTRY that APPLIES_TECHNOLOGY to im…
      …nts A_STEPPING_STONE in exploring THE_INTERACTION between FINTECH and its yet unfolding SOCIAL_AND_POLITICAL_CONTEXT
      …N in_the_past_few_years reflected by THE_EMERGENCE of ' ' FINTECH , ' ' which represents THE_MARRIAGE of ' ' FINANCE ' ' an…
                                                             ' ' FINTECH provides OPPORTUNITIES for THE_CREATION of NEW_SERVICES a…
                                                     therefore , FINTECH has become A_SUBJECT of DEBATE among PRACTITIONERS , INVE…
       …press including THE_SUBJECTS discussed in the context of FINTECH
                in doing so , we extend THE_GROWING_KNOWLEDGE on FINTECH and contribute to A_COMMON_UNDERSTANDING in THE_FINANCIAL…
                                    ) , who explore THE_FIELD of FINTECH


"""

from tm2p import Field
from tm2p._intern import ParamsMixin

__reviewed__ = "2026-01-29"


class ConcordanceUppercase(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        from tm2p.discov.concord import ConcordanceUser

        return (
            ConcordanceUser()
            .update(**self.params.__dict__)
            .with_source_field(Field.ABSTR_UPPER)
            .run()
        )
