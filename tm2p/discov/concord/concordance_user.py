"""
Concordance User
=========================================================================================

Smoke test:
    >>> from tm2p import CorpusField, RecordsOrderBy
    >>> from tm2p.analyze.concordances import ConcordanceUser
    >>> contexts = (
    ...     ConcordanceUser()
    ...     #
    ...     .with_field(CorpusField.ABS_RAW)
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
    >>> assert isinstance(contexts, list)
    >>> assert len(contexts) > 0
    >>> assert all(isinstance(c, str) for c in contexts)
    >>> for t in contexts[:10]: print(t)
             There is currently no consensus about what the term FINTECH means
      …ing more than 200 scholarly articles referencing the term FINTECH and covering a period of more than 40 years
      …nition concentrates on extracting out the quintessence of FINTECH using both spheres
      …eerreviewed definitions of the term, it is concluded that FINTECH is a new financial industry that applies technology to im…
       …historical development of China's financial technology ( FINTECH ) industry
      …nts a stepping stone in exploring the interaction between FINTECH and its yet unfolding social and political context
               It also discusses policy implications for China's FINTECH industry, focusing on the changing role of the state in f…
      …ion in the past few years reflected by the emergence of “ FINTECH ,” which represents the marriage of “finance” and “inform…
                                                               ” FINTECH provides opportunities for the creation of new services a…
                                                      Therefore, FINTECH has become a subject of debate among practitioners, inves…


"""

import re

import pandas as pd  # type: ignore

from tm2p import CorpusField
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

__reviewed__ = "2026-01-29"


class ConcordanceUser(
    ParamsMixin,
):
    """:meta private:"""

    def _extract_context_phrases(self, dataframe: pd.DataFrame) -> pd.Series:

        search_for = self.params.pattern.lower().replace("_", " ")

        dataframe = dataframe.set_index(
            pd.Index(
                dataframe[CorpusField.RID.value]
                + " / "
                + dataframe[CorpusField.TITLE_RAW.value]
            )
        )

        dataframe["_found_"] = (
            dataframe[self.params.source_field.value]
            .astype(str)
            .str.contains(r"\b" + search_for + r"\b", regex=True, flags=re.IGNORECASE)
        )

        dataframe = dataframe[dataframe["_found_"]]
        abstracts = dataframe[self.params.source_field.value]
        phrases = abstracts.str.replace(";", ".").str.split(".").explode().str.strip()
        context_phrases = phrases[
            phrases.str.contains(
                r"\b" + search_for + r"\b", regex=True, flags=re.IGNORECASE
            )
        ]

        return context_phrases

    # -------------------------------------------------------------------------
    def _create_contexts_dataframe(self, context_phrases: pd.Series) -> pd.DataFrame:

        search_for = self.params.pattern.lower().replace("_", " ")

        regex = r"\b" + search_for + r"\b"
        contexts = context_phrases.str.extract(
            r"(?P<left_context>[\s \S]*)" + regex + r"(?P<right_context>[\s \S]*)",
            flags=re.IGNORECASE,
        )

        contexts["left_context"] = contexts["left_context"].fillna("")
        contexts["left_context"] = contexts["left_context"].str.strip()

        contexts["right_context"] = contexts["right_context"].fillna("")
        contexts["right_context"] = contexts["right_context"].str.strip()

        contexts = contexts[
            contexts["left_context"].map(lambda x: x != "")
            | contexts["right_context"].map(lambda x: x != "")
        ]

        return contexts

    # -------------------------------------------------------------------------
    def _transform_context_dataframe_to_texts(
        self, contexts: pd.DataFrame
    ) -> list[str]:

        search_for = self.params.pattern
        contexts = contexts.copy()
        contexts["left_r"] = contexts["left_context"].str[::-1]

        contexts["left_context"] = contexts["left_context"].map(
            lambda x: "<<<" + x[-57:] if len(x) > 60 else x
        )
        contexts["right_context"] = contexts["right_context"].map(
            lambda x: x[:57] + ">>>" if len(x) > 60 else x
        )

        contexts["left_context"] = contexts["left_context"].str.replace(
            r"(<<<\s*)", "\u2026", regex=True
        )

        contexts["right_context"] = contexts["right_context"].str.replace(
            r"(\s*>>>)", "\u2026", regex=True
        )

        texts = []
        for _, row in contexts.iterrows():
            text = (
                f"{row['left_context']:>60} {search_for.upper()} {row['right_context']}"
            )
            texts.append(text)

        return texts

    # -------------------------------------------------------------------------
    def run(self) -> list[str]:

        dataframe = load_filtered_main_csv_zip(params=self.params)
        context_phrases = self._extract_context_phrases(dataframe=dataframe)
        contexts_dataframe = self._create_contexts_dataframe(context_phrases)
        texts = self._transform_context_dataframe_to_texts(contexts_dataframe)
        return texts
