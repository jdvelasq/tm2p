"""
Main Path Documents
===============================================================================

Smoke tests:
    >>> from tm2p import RecordOrderBy
    >>> from tm2p.synthes.main_path import MainPathDocuments
    >>> df = (
    ...     MainPathDocuments()
    ...     #
    ...     # ANALYSIS UNIT:
    ...     .having_items_in_top(None)
    ...     .having_citation_threshold(0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     #
    ...     .run()
    ... )
    >>> len(df)
    5
    >>> print(df[0])
    UT 97
    AR Zabat, 2024, WSEAS TRANS BUS ECON, V21, P1200
    TI The Impact of RegTech on Compliance Costs and Risk Management from the
       Perspective of Saudi Banks' Employees
    AU Zabat L.; Sadaoui N.; Benlaria H.; Ahmed S.A.K.; Hussien B.S.A.; Abdulrahman
       B.M.A.
    TC 2
    SO WSEAS TRANS BUS ECON
    PY 2024
    AB through this_research , we will be analyzing THE_EFFECT of REGTECH on
       COMPLIANCE_COSTS and RISK_MANAGEMENT in THE_BANKING_SECTOR , mainly with the
       eye of PEOPLE in administrative roles in saudi BANKS , a_total_of 232. a
       NEW_TECHNOLOGICAL trend is reshaping THE_FINANCIAL_INDUSTRY , REGTECH ,
       marked by various advanced technological PROCESSES and AUTOMATION .
       THE_MAIN_FINDINGS show that REGTECH significantly reduces COMPLIANCE_COSTS ,
       confirming its COST_SAVING_POTENTIAL . therefore , employee PERCEPTIONS are
       critical to integrating and adopting REGTECH within BUSINESS_OPERATIONS . in
       addition , REGTECH improves RISK_MANAGEMENT_SYSTEMS with more accessible
       PROCEDURES and better INTERNAL_CONTROLS . this proves REGTECH ' s ABILITY to
       improve the BANKING_PROCESSES and strengthen the RISK_MANAGEMENT_SYSTEM .
       proportional to the organizational SUPPORT , tool INVESTMENTS , and tool
       diversity INTERACTIONS are moderated , and operational EFFICIENCY is
       enhanced . this_research contributes significantly to the more profound
       KNOWLEDGE of the implication of REGTECH in the saudi BANKING sector , which
       facilitates TRANSFORMATION through renewed PRACTICES in THE_INDUSTRY
       alongside its EFFICIENCY . 2024 , world scientific and engineering academy
       and society . all rights reserved .
    DE banking sector; compliance costs; employee perspectives; financial
       institutions; internal controls; operational efficiency; regtech; risk
       management; saudi arabia; technology adoption
    <BLANKLINE>





"""

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p.ingest.rec import RecordViewer
from tm2p.synthes.main_path._intern.compute_main_path import compute_main_path


class MainPathDocuments(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        """:meta private:"""

        #
        # Creates a table with citing and cited articles
        articles_in_main_path, _ = compute_main_path(params=self.params)

        #
        # remove counters
        articles_in_main_path = [
            " ".join(article.split(" ")[:-1]) for article in articles_in_main_path
        ]

        #
        # build the filter
        records_match = {Field.RID: articles_in_main_path}

        documents = (
            RecordViewer()
            .update(**self.params.__dict__)
            .where_records_match(records_match)
            .run()
        )

        return documents
