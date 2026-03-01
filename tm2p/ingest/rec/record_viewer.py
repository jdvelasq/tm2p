"""
RecordViewer
=======================================================================================


Smoke tests:
    >>> # Countries:
    >>> from tm2p.refine.thesaurus_old.countries import (
    ...     InitializeThesaurus as CreateCountryThesaurus,
    ...     ApplyThesaurus as ApplyCountryThesaurus,
    ... )
    >>> CreateCountryThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyCountryThesaurus(root_directory="examples/fintech/", quiet=True).run()


    >>> # Organizations:
    >>> from tm2p.refine.thesaurus_old.organizations import (
    ...     InitializeThesaurus as CreateOrganizationsThesaurus,
    ...     ApplyThesaurus as ApplyOrganizationsThesaurus,
    ... )
    >>> CreateOrganizationsThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyOrganizationsThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Descriptors:
    >>> from tm2p.refine.thesaurus_old.descriptors import (
    ...     InitializeThesaurus as CreateDescriptorsThesaurus,
    ...     ApplyThesaurus as ApplyDescriptorsThesaurus,
    ... )
    >>> CreateDescriptorsThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyDescriptorsThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> from tm2p.explore import RecordViewer
    >>> # Create, configure, and run the viewer
    >>> # order_records_by:
    >>> #   date_newest, date_oldest, global_cited_by_highest, global_cited_by_lowest
    >>> #   local_cited_by_highest, local_cited_by_lowest, first_author_a_to_z
    >>> #   first_author_z_to_a, source_title_a_to_z, source_title_z_to_a
    >>> #
    >>> # For most global cited documents use:
    >>> #    .where_database_is("main")
    >>> #    .where_records_ordered_by("global_cited_by_highest")
    >>> #
    >>> # For most local cited documents use:
    >>> #    .where_database_is("main")
    >>> #    .where_records_ordered_by("local_cited_by_highest")
    >>> #
    >>> # For most global cited references use:
    >>> #    .where_database_is("references")
    >>> #    .where_records_ordered_by("global_cited_by_highest")
    >>> #
    >>> # For most local cited references use:
    >>> #    .where_database_is("references")
    >>> #    .where_records_ordered_by("local_cited_by_highest")
    >>> #
    >>> viewer = (
    ...     RecordViewer()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by("global_cited_by_highest")
    ... )
    >>> documents = viewer.run()

    >>> len(documents)
    50

    >>> with open("examples/fintech/record_viewer.txt", "w", encoding="utf-8") as f:
    ...     for doc in documents:
    ...         print(doc, file=f)
    ...         print(file=f)

    >>> print(documents[0]) # doctest: +SKIP
    UT 30
    AR Gomber P., 2018, J MANAGE INF SYST, V35, P220
    TI On the Fintech Revolution: Interpreting the Forces of Innovation,
       Disruption, and Transformation in Financial Services
    AU Gomber P.; Kauffman R.J.; Parker C.; Weber B.W.
    TC 576
    SO Journal of Management Information Systems
    PY 2018
    AB THE_FINANCIAL_SERVICES_INDUSTRY has been experiencing THE_RECENT_EMERGENCE
       of NEW_TECHNOLOGY_INNOVATIONS and PROCESS_DISRUPTIONS . THE_INDUSTRY overall
       , and MANY_FINTECH_START_UPS are looking for NEW_PATHWAYS to
       SUCCESSFUL_BUSINESS_MODELS , THE_CREATION of ENHANCED_CUSTOMER_EXPERIENCE ,
       and approaches that result in SERVICES_TRANSFORMATION . INDUSTRY and
       ACADEMIC_OBSERVERS believe this to be more of A_REVOLUTION than A_SET of
       LESS_INFLUENTIAL_CHANGES , with FINANCIAL_SERVICES as A_WHOLE due for
       MAJOR_IMPROVEMENTS in EFFICIENCY , CUSTOMER_CENTRICITY , and INFORMEDNESS .
       THE_LONG_STANDING_DOMINANCE of LEADING_FIRMS that are not able to figure out
       how to effectively hook up with THE_FINTECH_REVOLUTION is at STAKE . we
       present A_NEW_FINTECH_INNOVATION_MAPPING_APPROACH that enables
       THE_ASSESSMENT of THE_EXTENT to which there are CHANGES and TRANSFORMATIONS
       in FOUR_AREAS of FINANCIAL_SERVICES . we discuss : OPERATIONS_MANAGEMENT in
       FINANCIAL_SERVICES and THE_CHANGES occurring . TECHNOLOGY_INNOVATIONS that
       have begun to leverage THE_EXECUTION and STAKEHOLDER_VALUE associated with
       PAYMENTS , CRYPTOCURRENCIES , BLOCKCHAIN , and CROSS_BORDER_PAYMENTS .
       MULTIPLE_INNOVATIONS that have affected LENDING_AND_DEPOSIT_SERVICES ,
       PEER_TO_PEER ( P2P ) LENDING , and SOCIAL_MEDIA_USE . ISSUES with_respect_to
       INVESTMENTS , FINANCIAL_MARKETS , TRADING , RISK_MANAGEMENT , ROBO_ADVISORY
       and SERVICES influenced by BLOCKCHAIN and FINTECH_INNOVATIONS . copyright
       taylor and francis group , llc .
    ID BLOCKCHAIN; COMMERCE; RISK_MANAGEMENT; BUSINESS_MODELS; CUSTOMER_EXPERIENCE;
       FINANCIAL_SERVICE; FINANCIAL_SERVICES_INDUSTRIES; NEW_TECHNOLOGIES;
       OPERATIONS_MANAGEMENT; STAKEHOLDER_VALUES; TECHNOLOGY_INNOVATION; FINANCE
    <BLANKLINE>




"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)
from tm2p._intern.rec_build import dicts_to_strings


class RecordViewer(ParamsMixin):
    """:meta private:"""

    def run(self):

        dataframe = load_filtered_main_csv_zip(params=self.params)
        string_list = dicts_to_strings(dataframe)
        return string_list
