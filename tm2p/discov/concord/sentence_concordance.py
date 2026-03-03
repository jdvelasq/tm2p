"""
SentenceConcordance
=========================================================================================

Smoke test:
    >>> from tm2p import RecordOrderBy
    >>> from tm2p.discov.concord import SentenceConcordance
    >>> sentences = (
    ...     SentenceConcordance()
    ...     .having_text_matching("FINTECH")
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     #
    ...     .run()
    ... )
    >>> assert isinstance(sentences, list)
    >>> assert len(sentences) > 0
    >>> assert all(isinstance(s, str) for s in sentences)
    >>> for t in sentences[:10]: print(t)
    FINANCIAL_TECHNOLOGY [ FINTECH ] ) and THE_FINANCIAL_PERFORMANCE , i .
    this_research_delves into THE_TRANSFORMATIVE_POTENTIAL of integrating FINANCIAL_TECHNOLOGY ( FINTECH ) and BLOCKCHAIN in GREEN_FINANCE .
    purpose : the_purpose_of_this_study_is_to discuss the UNITED_ARAB_EMIRATES ' ( UAE ) FAVORABLE_ATTITUDE toward THE_FINANCIAL_SECTOR_DIGITAL_TRANSFORMATION and THE_DEVELOPMENT of FINTECH due_to_the rise of FINANCIAL_TECHNOLOGY .
    FINTECH blends INNOVATION_AND_TECHNOLOGY to provide FINANCIAL_INCLUSION to STAKEHOLDERS through VARIOUS_NEW_PRODUCTS and SERVICES SUCH_METAVERSE and ARTIFICIAL_INTELLIGENCE .
    originality / value : this_study_is critical because_the UAE_BANKING sector serves DIVERSE_NATIONALITIES , and ITS_SUCCESS is contingent on FINTECH and ITS_COMPETITIVE_EDGE .
    in_recent_years , THE_PROGRESS in FINTECH has emerged A_SIGNIFICANT_SOURCE to decline THE_ENERGY which turns to enhance THE_ENVIRONMENTAL_QUALITY .
    FINTECH has confirmed THE_SIGNIFICANT_AND_POSITIVE_RELATIONSHIP with GREEN_ENVIRONMENTAL_INDEX .
    THE_THREE_SUBCATEGORIES of FINTECH , FINANCIAL_BREADTH , FINANCIAL_DEPTH , and FINANCIAL_DIGITALIZATION , have POSITIVE_INFLUENCE to promote THE_GREEN_ENVIRONMENTAL_INDEX .
    HETEROGENEITY_TEST has reported THE_STRONG_IMPACT of FINTECH for THREE_CHINESE_REGIONS .
    in case of GREEN_FINANCING_MEDIATION , FINTECH has reported THE_PARTIAL_MEDIATION of GREEN_CREDIT and GREEN_INVESTMENT to influence THE_GREEN_ENVIRONMENTAL_INDEX .


"""

import re

import pandas as pd  # type: ignore
from textblob import TextBlob  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

__reviewed__ = "2026-01-29"


class SentenceConcordance(
    ParamsMixin,
):
    """:meta private:"""

    def _get_search_pattern(self) -> str:
        pattern = self.params.pattern
        if isinstance(pattern, tuple):
            pattern = pattern[0]
        return r"\b" + re.escape(pattern.lower().replace("_", " ")) + r"\b"

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
        filtered_dataframe = dataframe[found]
        abstracts = filtered_dataframe[Field.ABSTR_UPPER.value]
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
