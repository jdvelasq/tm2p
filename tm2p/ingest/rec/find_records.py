"""
Find records
===============================================================================

Smoke tests:
    >>> from tm2p import Field, RecordOrderBy
    >>> from tm2p.ingest.rec import FindRecords
    >>> docs = (
    ...     FindRecords()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     #
    ...     # SEARCH:
    ...     .having_text_matching('regtech')
    ...     .having_regex_search(False)
    ...     .having_case_sensitive(False)
    ...     .having_regex_flags(0)
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...      #
    ...      .run()
    ... )
    >>> isinstance(docs, list)
    True
    >>> print(docs[0])
    UT 46
    AR Muganyi, 2022, FINANC INNOV, V8
    TI Fintech, regtech, and financial development: evidence from China
    AU Muganyi T.; Yan L.; Yin Y.; Sun H.; Gong X.; Taghizadeh-Hesary F.
    TC 139
    SO FINANC INNOV
    PY 2022
    AB this_study_investigates_the_influence_of FINTECH on DEVELOPMENTS in CHINA '
       s FINANCIAL_SECTOR across 290 CITIES and 31 provinces between 2011 and 2018
       . using a TWO_STAGE_LEAST_SQUARES_INSTRUMENTAL_VARIABLE_REGRESSION_APPROACH
       and correcting for CROSS_SECTIONAL_DEPENDENCY , SIMULTANEITY , and
       ENDOGENEITY of REGRESSORS , the_results establish A_POSITIVE_LINK between
       FINTECH and FINANCIAL_DEVELOPMENT . our_findings_show_that
       FINTECH_SUPPORTS_FINANCIAL_SECTOR_DEVELOPMENT by enhancing ACCESS ( LOANS )
       , DEPTH ( deposits ) , and SAVINGS within CHINA ' s FINANCIAL_INSTITUTIONS .
       we also show that THE_EMERGENCE of FINTECH in THE_AREA of
       FINANCIAL_REGULATION ( REGULATORY_TECHNOLOGY : REGTECH ) can significantly
       improve FINANCIAL_DEVELOPMENT_OUTCOMES . therefore , it is imperative for
       REGULATORS to PURSUE_POLICIES that BALANCE_GROWTH in THE_FINTECH_SECTOR
       while mitigating THE_ASSOCIATED_RISKS . in addition , we_use the
       DIFFERENCE_IN_DIFFERENCES_APPROACH to show that POLICY_MEASURES such as
       INTEREST_RATES_LIBERALIZATION also positively impacted FINANCIAL_DEVELOPMENT
       during THE_ANALYSIS_PERIOD . in OUR_CONCLUSION , we_suggest
       A_POLICY_FRAMEWORK for BALANCED_FINTECH_SECTOR_GROWTH in
       DEVELOPING_COUNTRIES . 2022 , the author ( s ) .
    DE China; Financial development; Fintech; Regtech
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)
from tm2p._intern.rec_build import dicts_to_strings, records_to_dicts


class FindRecords(ParamsMixin):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _filter_records(self, records):

        records = records.copy()
        records = records.dropna(subset=[self.params.source_field.value])
        records["_order_"] = range(len(records))

        if isinstance(self.params.pattern, str):
            patterns = (self.params.pattern,)
        else:
            patterns = self.params.pattern

        selected = set()
        for pattern in patterns:

            contains = records[self.params.source_field.value].str.contains(
                pat=pattern,
                case=self.params.case_sensitive,
                flags=self.params.regex_flags,
                regex=self.params.regex_search,
            )
            selected.update(records[contains]["_order_"].tolist())

        records = records[records["_order_"].isin(selected)].drop(columns="_order_")

        return records

    # -------------------------------------------------------------------------
    def run(self):

        records = load_filtered_main_csv_zip(params=self.params)
        records = self._filter_records(records)
        mapping = records_to_dicts(records)
        documents = dicts_to_strings(mapping)

        return documents
