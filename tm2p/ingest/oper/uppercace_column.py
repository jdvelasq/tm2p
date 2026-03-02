"""
UppercaseColumn
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import UppercaseColumn
    >>> (
    ...     UppercaseColumn()
    ...     #
    ...     # FIELDS:
    ...     .with_source_field(Field.ABSTR_TOK)
    ...     .with_target_field(Field.USR0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     #
    ...     .run()
    ... )

    >>> from tm2p.ingest.oper import Query
    >>> df = (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
    >>> import textwrap
    >>> print(textwrap.fill(df.values[1][0], width=90))
    FINTECH_APPLICATIONS are examined as CATALYSTS for revolutionizing GREEN_FINANCE ,
    showcasing THEIR_CAPACITY to STREAMLINE_PROCESSES , FACILITATE_TRANSPARENT_TRANSACTIONS ,
    and provide PERSONALIZED_INVESTMENT_OPTIONS . THE_FUNCTIONALITIES of THESE_APPLICATIONS
    are dissected , emphasizing THEIR_ROLE in mitigating BARRIERS such as
    INFORMATION_ASYMMETRY and INEFFICIENCIES in FUND_DISTRIBUTION . BLOCKCHAIN ' s
    decentralized LEDGER_SYSTEM is analyzed for ITS_ABILITY to ENHANCE_TRUST and TRANSPARENCY
    in SUSTAINABLE_INVESTMENT . it HIGHLIGHTS_SUCCESSFUL_IMPLEMENTATIONS of BLOCKCHAIN in
    SUSTAINABLE_FINANCE , illuminating ITS_PRACTICAL_BENEFITS in overcoming LIMITATIONS like
    FRAUD_RISK and reducing ADMINISTRATIVE_COSTS . this_research_delves into
    THE_TRANSFORMATIVE_POTENTIAL of integrating FINANCIAL_TECHNOLOGY ( FINTECH ) and
    BLOCKCHAIN in GREEN_FINANCE . by transcending TRADITIONAL_BARRIERS , THESE_TECHNOLOGIES
    not only enrich THE_FUNCTIONALITIES of APPLICATIONS but also OPEN_NEW_HORIZONS for
    SUSTAINABLE_INVESTMENT , paving THE_WAY for
    A_MORE_RESILIENT_AND_ENVIRONMENTALLY_CONSCIOUS_FINANCIAL_FUTURE . 2024 , igi global .



"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.upperc_keyterm import uppercase_keyterms
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class UppercaseColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.target_field}` is protected")

        uppercase_keyterms(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )


#
