"""
RecordTermSearch
=========================================================================================

Smoke test:
    >>> from tm2p import RecordOrderBy
    >>> from tm2p.discov.concord import RecordTermSearch
    >>> mapping = (
    ...     RecordTermSearch()
    ...     #
    ...     .having_text_matching("FINTECH")
    ...     #
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     .run()
    ... )
    >>> assert isinstance(mapping, list)
    >>> assert len(mapping) > 0
    >>> assert all(isinstance(r, dict) for r in mapping)
    >>> assert 'AR' in mapping[0]
    >>> assert 'AU' in mapping[0]
    >>> from pprint import pprint
    >>> pprint(mapping[0])
    {'AB': 'purpose : this_study_aims_to_examine_the_relationship_between the '
           'DIFFUSION_OF_TECHNOLOGY enabled INNOVATION_IN_FINANCIAL_SERVICES ( i . '
           'e . FINANCIAL_TECHNOLOGY [ FINTECH ] ) and THE_FINANCIAL_PERFORMANCE , '
           'i . e . PROFITABILITY and MARKET_VALUE of THE_BANKS listed in the '
           'GULF_COOPERATION_COUNCIL ( gcc ) COUNTRIES . design / methodology / '
           'approach : AN_EXTENSIVE_REVIEW of THE_LITERATURE was carried out , and '
           'A_DIFFUSION_INDEX of 73 items including was adopted to measure '
           'THE_LEVEL of FINTECH_USAGE or DIFFUSION for THE_BANKS that are listed '
           'on THE_GCC_STOCK_EXCHANGES . the_study used RETURN_ON_ASSETS ( ROA ) '
           'and TOBIN_Q ( tq ) as PROXIES to measure PROFITABILITY and '
           'MARKET_VALUE , respectively . findings : the_findings of the empirical '
           'results_indicate_that_there_is_a POSITIVE_RELATIONSHIP between '
           'FINTECH_IMPLEMENTATION and MARKET_PERFORMANCE ( tq ) in THE_GCC_BANKS '
           '. the_results also showed that THE_HIGHEST_LEVEL of '
           'FINTECH_IMPLEMENTATION was 79.7 % by UNITED_ARAB_EMIRATES_BANKS '
           'followed by BAHRAINI_BANKS at 76.7 % based on THE_INDEX developed for '
           'this_study . practical implications : this_study , hence , recommends '
           'that POLICYMAKERS and GOVERNMENTS implement SUPPORTIVE_POLICIES and '
           'INITIATIVES , allowing CONSUMERS to EMBRACE_TECHNOLOGY as part of '
           'THEIR_WAY of LIFE . this ENCOURAGES_BANKS and OTHER_ORGANIZATIONS to '
           'FORMULATE_STRATEGIES that integrate TECHNOLOGY into OPERATIONS . '
           'originality / value : this_paper_offers NEW_CONTRIBUTIONS to '
           'THE_GCC_LITERATURE regarding FINANCIAL_TECHNOLOGY and provides '
           'RECOMMENDATIONS to THE_GCC_FINANCIAL_INSTITUTIONS , FINANCIAL_MARKETS '
           ', POLICYMAKERS and GOVERNMENTS . 2024 , emerald publishing limited .',
     'AR': 'Al-Sartawi, 2024, J FINANC REPORT ACCOUNT',
     'AU': 'Al-Sartawi A.',
     'DE': 'digital transformation; financial sector; fintech; fintech governance; '
           'fintech strategies; firm market value; gcc countries; profitability',
     'ID': nan,
     'PY': 2024,
     'SO': 'J FINANC REPORT ACCOUNT',
     'TC': 125,
     'TI': 'The diffusion of financial technology-enabled innovation in GCC-listed '
           'banks and its relationship with profitability and market value',
     'UT': 13}




"""

import re

import pandas as pd  # type: ignore
from textblob import TextBlob  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access.load_filtered_main_csv_zip import (
    load_filtered_main_csv_zip,
)
from tm2p._intern.rec_build import records_to_dicts

__reviewed__ = "2026-01-29"


class RecordTermSearch(ParamsMixin):
    """:meta private:"""

    def _filter_by_concordance(
        self, dataframe: pd.DataFrame, search_for: str
    ) -> pd.DataFrame:

        found = (
            dataframe[Field.ABSTR_TOK.value]
            .astype(str)
            .str.contains(search_for, regex=True)
        )
        dataframe = dataframe.loc[found, :]
        return dataframe

    def _process_abstracts(
        self, dataframe: pd.DataFrame, search_for: str
    ) -> pd.DataFrame:

        dataframe = dataframe.copy()

        dataframe[Field.ABSTR_TOK.value] = dataframe[Field.ABSTR_TOK.value].apply(
            lambda x: list(TextBlob(x).sentences)  # type: ignore
        )
        dataframe[Field.ABSTR_TOK.value] = dataframe[Field.ABSTR_TOK.value].apply(
            lambda x: [str(y) for y in x]
        )
        dataframe[Field.ABSTR_TOK.value] = dataframe[Field.ABSTR_TOK.value].apply(
            lambda x: [y[:-2] if y[-2:] == " ." else y for y in x]
        )
        dataframe[Field.ABSTR_TOK.value] = dataframe[Field.ABSTR_TOK.value].apply(
            lambda x: [y for y in x if re.search(search_for, y)]
        )
        dataframe[Field.ABSTR_TOK.value] = dataframe[Field.ABSTR_TOK.value].map(
            " . ".join
        )

        return dataframe

    def run(self) -> list[dict]:

        pattern = (
            self.params.pattern[0]
            if isinstance(self.params.pattern, tuple)
            else self.params.pattern
        )
        search_for = r"\b" + pattern.lower().replace("_", " ") + r"\b"
        dataframe = load_filtered_main_csv_zip(params=self.params)
        dataframe = self._filter_by_concordance(dataframe, search_for)
        dataframe = self._process_abstracts(dataframe, search_for)
        mapping = records_to_dicts(dataframe)

        return mapping
