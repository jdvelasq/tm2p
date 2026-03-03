"""
RecordViewer
=======================================================================================

Smoke tests:
    >>> from tm2p import RecordOrderBy
    >>> from tm2p.ingest.rec import RecordViewer
    >>> docs = (
    ...     RecordViewer()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     .run()
    ... )
    >>> len(docs)
    180
    >>> print(docs[0])
    UT 13
    AR Al-Sartawi, 2024, J FINANC REPORT ACCOUNT
    TI The diffusion of financial technology-enabled innovation in GCC-listed banks
       and its relationship with profitability and market value
    AU Al-Sartawi A.
    TC 125
    SO J FINANC REPORT ACCOUNT
    PY 2024
    AB purpose : this_study_aims_to_examine_the_relationship_between the
       DIFFUSION_OF_TECHNOLOGY enabled INNOVATION_IN_FINANCIAL_SERVICES ( i . e .
       FINANCIAL_TECHNOLOGY [ FINTECH ] ) and THE_FINANCIAL_PERFORMANCE , i . e .
       PROFITABILITY and MARKET_VALUE of THE_BANKS listed in the
       GULF_COOPERATION_COUNCIL ( gcc ) COUNTRIES . design / methodology / approach
       : AN_EXTENSIVE_REVIEW of THE_LITERATURE was carried out , and
       A_DIFFUSION_INDEX of 73 items including was adopted to measure THE_LEVEL of
       FINTECH_USAGE or DIFFUSION for THE_BANKS that are listed on
       THE_GCC_STOCK_EXCHANGES . the_study used RETURN_ON_ASSETS ( ROA ) and
       TOBIN_Q ( tq ) as PROXIES to measure PROFITABILITY and MARKET_VALUE ,
       respectively . findings : the_findings of the empirical
       results_indicate_that_there_is_a POSITIVE_RELATIONSHIP between
       FINTECH_IMPLEMENTATION and MARKET_PERFORMANCE ( tq ) in THE_GCC_BANKS .
       the_results also showed that THE_HIGHEST_LEVEL of FINTECH_IMPLEMENTATION was
       79.7 % by UNITED_ARAB_EMIRATES_BANKS followed by BAHRAINI_BANKS at 76.7 %
       based on THE_INDEX developed for this_study . practical implications :
       this_study , hence , recommends that POLICYMAKERS and GOVERNMENTS implement
       SUPPORTIVE_POLICIES and INITIATIVES , allowing CONSUMERS to
       EMBRACE_TECHNOLOGY as part of THEIR_WAY of LIFE . this ENCOURAGES_BANKS and
       OTHER_ORGANIZATIONS to FORMULATE_STRATEGIES that integrate TECHNOLOGY into
       OPERATIONS . originality / value : this_paper_offers NEW_CONTRIBUTIONS to
       THE_GCC_LITERATURE regarding FINANCIAL_TECHNOLOGY and provides
       RECOMMENDATIONS to THE_GCC_FINANCIAL_INSTITUTIONS , FINANCIAL_MARKETS ,
       POLICYMAKERS and GOVERNMENTS . 2024 , emerald publishing limited .
    DE Digital transformation; Financial sector; FinTech; FinTech governance;
       FinTech strategies; Firm market value; GCC countries; Profitability
    <BLANKLINE>




"""

from tm2p._intern import ParamsMixin
from tm2p._intern.rec_build import dicts_to_strings
from tm2p.ingest.rec import RecordMapping


class RecordViewer(ParamsMixin):
    """:meta private:"""

    def run(self):

        mapping = RecordMapping().update(**self.params.__dict__).run()
        string_list = dicts_to_strings(mapping)
        return string_list
