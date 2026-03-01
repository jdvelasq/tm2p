"""
Find records
===============================================================================


Smoke tests:
    >>> from tm2p.database.search import FindRecords

    >>> # Create, configure, and run the finder
    >>> finder = (
    ...     FindRecords()
    ...     #
    ...     # FIELD:
    ...     .with_field("author_keywords")
    ...     #
    ...     # SEARCH:
    ...     .with_field_pattern('REGTECH')
    ...     .having_regex_search(False)
    ...     .having_case_sensitive(False)
    ...     .having_regex_flags(0)
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by("date_newest")
    ... )
    >>> docs = finder.run()
    >>> print(docs[0]) # doctest: +SKIP
    UT 26
    AR Haddad C., 2019, SMALL BUS ECON, V53, P81
    TI The emergence of the global fintech market: economic and technological
       determinants
    AU Haddad C.; Hornuf L.
    TC 258
    SO Small Business Economics
    PY 2019
    AB we investigate THE_ECONOMIC_AND_TECHNOLOGICAL_DETERMINANTS inducing
       ENTREPRENEURS to establish VENTURES with THE_PURPOSE of reinventing
       FINANCIAL_TECHNOLOGY ( FINTECH ) . we find that COUNTRIES witness
       MORE_FINTECH_STARTUP_FORMATIONS when THE_ECONOMY is well developed and
       VENTURE_CAPITAL is readily available . furthermore , THE_NUMBER of
       SECURE_INTERNET_SERVERS , MOBILE_TELEPHONE_SUBSCRIPTIONS , and
       THE_AVAILABLE_LABOR_FORCE has A_POSITIVE_IMPACT on THE_DEVELOPMENT of
       THIS_NEW_MARKET_SEGMENT . finally , the more difficult it is for COMPANIES
       to ACCESS_LOANS , the higher is THE_NUMBER of FINTECH_STARTUPS in A_COUNTRY
       . overall , THE_EVIDENCE suggests that FINTECH_STARTUP_FORMATION_NEED not be
       left to chance , but ACTIVE_POLICIES can influence THE_EMERGENCE of
       THIS_NEW_SECTOR . 2018 , the author ( s ) .
    DE ENTREPRENEURSHIP; FINANCIAL_INSTITUTIONS; FINTECH; STARTUPS
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
    def _step_01_load_the_database(self):
        return load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def _step_02_filter_the_records(self, records):

        records = records.copy()
        records = records.dropna(subset=[self.params.source_field])

        contains = records[self.params.source_field].str.contains(
            pat=self.params.pattern,
            case=self.params.case_sensitive,
            flags=self.params.regex_flags,
            regex=self.params.regex_search,
        )

        records = records.loc[contains.index, :]

        return records

    # -------------------------------------------------------------------------
    def run(self):

        records = self._step_01_load_the_database()
        records = self._step_02_filter_the_records(records)
        mapping = records_to_dicts(records)
        documents = dicts_to_strings(mapping)

        return documents
