"""
RecordMapping
===============================================================================

Smoke Test:
    >>> from tm2p.explore import RecordMapping, RecordsOrderBy
    >>> mapping = (
    ...     RecordMapping()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordsOrderBy.GLOBAL_CITED_BY_HIGHEST)
    ...     .run()
    ... )

    >>> pprint(mapping[0])
    {'AB': 'THE_FINANCIAL_SERVICES_INDUSTRY has been experiencing '
           'THE_RECENT_EMERGENCE of NEW_TECHNOLOGY_INNOVATIONS and '
           'PROCESS_DISRUPTIONS . THE_INDUSTRY overall , and '
           'MANY_FINTECH_START_UPS are looking for NEW_PATHWAYS to '
           'SUCCESSFUL_BUSINESS_MODELS , THE_CREATION of '
           'ENHANCED_CUSTOMER_EXPERIENCE , and approaches that result in '
           'SERVICES_TRANSFORMATION . INDUSTRY and ACADEMIC_OBSERVERS believe this '
           'to be more of A_REVOLUTION than A_SET of LESS_INFLUENTIAL_CHANGES , '
           'with FINANCIAL_SERVICES as A_WHOLE due for MAJOR_IMPROVEMENTS in '
           'EFFICIENCY , CUSTOMER_CENTRICITY , and INFORMEDNESS . '
           'THE_LONG_STANDING_DOMINANCE of LEADING_FIRMS that are not able to '
           'figure out how to effectively hook up with THE_FINTECH_REVOLUTION is '
           'at STAKE . we present A_NEW_FINTECH_INNOVATION_MAPPING_APPROACH that '
           'enables THE_ASSESSMENT of THE_EXTENT to which there are CHANGES and '
           'TRANSFORMATIONS in FOUR_AREAS of FINANCIAL_SERVICES . we discuss : '
           'OPERATIONS_MANAGEMENT in FINANCIAL_SERVICES and THE_CHANGES occurring '
           '. TECHNOLOGY_INNOVATIONS that have begun to leverage THE_EXECUTION and '
           'STAKEHOLDER_VALUE associated with PAYMENTS , CRYPTOCURRENCIES , '
           'BLOCKCHAIN , and CROSS_BORDER_PAYMENTS . MULTIPLE_INNOVATIONS that '
           'have affected LENDING_AND_DEPOSIT_SERVICES , PEER_TO_PEER ( P2P ) '
           'LENDING , and SOCIAL_MEDIA_USE . ISSUES with_respect_to INVESTMENTS , '
           'FINANCIAL_MARKETS , TRADING , RISK_MANAGEMENT , ROBO_ADVISORY and '
           'SERVICES influenced by BLOCKCHAIN and FINTECH_INNOVATIONS . copyright '
           'taylor and francis group , llc .',
     'AR': 'Gomber P., 2018, J MANAGE INF SYST, V35, P220',
     'AU': 'Gomber P.; Kauffman R.J.; Parker C.; Weber B.W.',
     'DE': nan,
     'ID': 'BLOCKCHAIN; COMMERCE; RISK_MANAGEMENT; BUSINESS_MODELS; '
           'CUSTOMER_EXPERIENCE; FINANCIAL_SERVICE; FINANCIAL_SERVICES_INDUSTRIES; '
           'NEW_TECHNOLOGIES; OPERATIONS_MANAGEMENT; STAKEHOLDER_VALUES; '
           'TECHNOLOGY_INNOVATION; FINANCE',
     'PY': 2018,
     'SO': 'Journal of Management Information Systems',
     'TC': 576,
     'TI': 'On the Fintech Revolution: Interpreting the Forces of Innovation, '
           'Disruption, and Transformation in Financial Services',
     'UT': 30}


"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)
from tm2p._intern.rec_build import records_to_dicts


class RecordMapping(ParamsMixin):
    """:meta private:"""

    def run(self):

        records = load_filtered_main_csv_zip(params=self.params)
        mapping = records_to_dicts(records)
        return mapping
