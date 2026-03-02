"""
Concordance Tokenized
=========================================================================================

Smoke test:
    >>> from tm2p import RecordsOrderBy
    >>> from tm2p.analyze.concordances import ConcordanceTokenized
    >>> contexts = (
    ...     ConcordanceTokenized()
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
    >>> for t in contexts[:10]: print(t)
             there is currently no consensus about what the term FINTECH means
      …ing more than 200 scholarly articles referencing the term FINTECH and covering a period of more than 40 years
      …nition concentrates on extracting out the quintessence of FINTECH using both spheres
      …erreviewed definitions of the term , it is concluded that FINTECH is a new financial industry that applies technology to im…
      …istorical development of china ' s financial technology ( FINTECH ) industry
      …nts a stepping stone in exploring the interaction between FINTECH and its yet unfolding social and political context
             it also discusses policy implications for china ' s FINTECH industry , focusing on the changing role of the state in…
      …n in the past few years reflected by the emergence of ' ' FINTECH , ' ' which represents the marriage of ' ' finance ' ' an…
                                                             ' ' FINTECH provides opportunities for the creation of new services a…
                                                     therefore , FINTECH has become a subject of debate among practitioners , inve…


"""

from tm2p import Field
from tm2p._intern import ParamsMixin

__reviewed__ = "2026-01-29"


class ConcordanceTokenized(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        from tm2p.discov.concord import ConcordanceUser

        return (
            ConcordanceUser()
            .update(**self.params.__dict__)
            .with_source_field(Field.ABSTR_TOK)
            .run()
        )
