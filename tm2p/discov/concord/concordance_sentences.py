"""
Concordance Sentences
=========================================================================================

Smoke test:
    >>> from tm2p import RecordsOrderBy
    >>> from tm2p.analyze.concordances import ConcordanceSentences
    >>> sentences = (
    ...     ConcordanceSentences()
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
    >>> assert isinstance(sentences, list)
    >>> assert len(sentences) > 0
    >>> assert all(isinstance(s, str) for s in sentences)
    >>> for t in sentences[:10]: print(t)
    this_paper_explores THE_COMPLEXITY of FINTECH , and attempts A_DEFINITION , drawn from A_PROCESS of reviewing more than 200 scholarly articles referencing THE_TERM_FINTECH and covering A_PERIOD of more than 40 years .
    as THE_ORIGINS of THE_TERM can neither be unequivocally placed in ACADEMIA nor in PRACTICE , THE_DEFINITION concentrates on extracting out THE_QUINTESSENCE of FINTECH using BOTH_SPHERES .
    applying SEMANTIC_ANALYSIS and BUILDING on THE_COMMONALITIES of 13 peerreviewed DEFINITIONS of THE_TERM , it_is_concluded_that FINTECH is A_NEW_FINANCIAL_INDUSTRY that APPLIES_TECHNOLOGY to improve FINANCIAL_ACTIVITIES .
    this_research_represents A_STEPPING_STONE in exploring THE_INTERACTION between FINTECH and its yet unfolding SOCIAL_AND_POLITICAL_CONTEXT .
    THE_FINANCIAL_INDUSTRY has been strongly influenced by DIGITALIZATION in_the_past_few_years reflected by THE_EMERGENCE of ' ' FINTECH , ' ' which represents THE_MARRIAGE of ' ' FINANCE ' ' and ' ' INFORMATION_TECHNOLOGY . '
    ' FINTECH provides OPPORTUNITIES for THE_CREATION of NEW_SERVICES and BUSINESS_MODELS and poses CHALLENGES to TRADITIONAL_FINANCIAL_SERVICE_PROVIDERS .
    therefore , FINTECH has become A_SUBJECT of DEBATE among PRACTITIONERS , INVESTORS , and RESEARCHERS and is highly visible in THE_POPULAR_MEDIA .
    in_this_study , we unveil the drivers motivating the fintech phenomenon perceived by the english and german popular press including THE_SUBJECTS discussed in the context of FINTECH .
    in doing so , we extend THE_GROWING_KNOWLEDGE on FINTECH and contribute to A_COMMON_UNDERSTANDING in THE_FINANCIAL_AND_DIGITAL_INNOVATION_LITERATURE .
    , who explore THE_FIELD of FINTECH .


"""

import re

import pandas as pd  # type: ignore
from textblob import TextBlob  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

__reviewed__ = "2026-01-29"


class ConcordanceSentences(
    ParamsMixin,
):
    """:meta private:"""

    def _get_search_pattern(self) -> str:
        return r"\b" + re.escape(self.params.pattern.lower().replace("_", " ")) + r"\b"

    def _set_dataframe_index(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.set_index(
            pd.Index(
                dataframe[Field.RID.value] + " / " + dataframe[Field.TITLE_RAW.value]
            )
        )

    def _extract_abstracts_matching_pattern(
        self, dataframe: pd.DataFrame, search_for: str
    ) -> pd.Series:

        found = (
            dataframe[Field.ABSTR_UPPER.value]
            .astype(str)
            .str.contains(search_for, regex=True, flags=re.IGNORECASE)
        )
        dataframe = dataframe[found]
        abstracts = dataframe[Field.ABSTR_UPPER.value]
        return abstracts

    def _transform_abstracts_to_sentences(
        self,
        abstracts: pd.Series,
    ) -> pd.Series:

        abstracts = abstracts.str.replace(" ; ", " . ")
        abstracts = abstracts.apply(lambda x: [str(y) for y in TextBlob(x).sentences])  # type: ignore
        sentences = abstracts.explode()
        sentences = sentences.str.strip()

        return sentences

    def _select_sentences_matching_pattern(
        self,
        sentences: pd.Series,
        search_for: str,
    ) -> pd.Series:

        sentences = sentences[
            sentences.str.contains(search_for, regex=True, flags=re.IGNORECASE)
        ]

        return sentences

    def run(self) -> list[str]:

        search_for = self._get_search_pattern()
        dataframe = load_filtered_main_csv_zip(params=self.params)
        dataframe = self._set_dataframe_index(dataframe)
        abstracts = self._extract_abstracts_matching_pattern(dataframe, search_for)
        sentences = self._transform_abstracts_to_sentences(abstracts)
        sentences = self._select_sentences_matching_pattern(sentences, search_for)

        return sentences.tolist()
