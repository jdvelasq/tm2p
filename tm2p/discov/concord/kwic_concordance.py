"""
KWICConcordance
=========================================================================================

Smoke test:
    >>> from tm2p import Field, RecordOrderBy
    >>> from tm2p.discov.concord import KWICConcordance
    >>> contexts = (
    ...     KWICConcordance()
    ...     #
    ...     .with_source_field(Field.ABSTR_RAW)
    ...     .having_text_matching("FINTECH")
    ...     #
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     .where_records_ordered_by(RecordOrderBy.YEAR_NEWEST)
    ...     #
    ...     .run()
    ... )
    >>> assert isinstance(contexts, list)
    >>> assert len(contexts) > 0
    >>> assert all(isinstance(c, str) for c in contexts)
    >>> for t in contexts[:10]: print(t)
                                          financial technology [ FINTECH ]) and the financial performance, i
      …of 73 items including was adopted to measure the level of FINTECH usage or diffusion for the banks that are listed on the G…
      …ts indicate that there is a positive relationship between FINTECH implementation and market performance (TQ) in the GCC banks
               The results also showed that the highest level of FINTECH implementation was 79
                                                                 FINTECH applications are examined as catalysts for revolutionizin…
      …formative potential of integrating financial technology ( FINTECH ) and blockchain in green finance
      …al sector’s digital transformation and the development of FINTECH due to the rise of financial technology
                                                                 FINTECH blends innovation and technology to provide financial inc…
                            Findings: The findings indicate that FINTECH adoption had a substantial impact on the competitiveness…
                            The research indicates that adequate FINTECH implementation and alignment with technology management d…


"""

import re

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

__reviewed__ = "2026-01-29"


class KWICConcordance(
    ParamsMixin,
):
    """:meta private:"""

    def _extract_context_phrases(self, dataframe: pd.DataFrame) -> pd.Series:

        pattern = self.params.pattern
        if isinstance(pattern, tuple):
            pattern = pattern[0]

        search_for = pattern.lower().replace("_", " ")

        dataframe = dataframe.set_index(
            pd.Index(
                dataframe[Field.REC_ID.value] + " / " + dataframe[Field.TITLE_RAW.value]
            )
        )

        dataframe["_found_"] = (
            dataframe[self.params.source_field.value]
            .astype(str)
            .str.contains(r"\b" + search_for + r"\b", regex=True, flags=re.IGNORECASE)
        )

        dataframe = dataframe[dataframe["_found_"]].copy()  # type: ignore[assignment]
        abstracts = dataframe[self.params.source_field.value]
        phrases = abstracts.str.replace(";", ".").str.split(".").explode().str.strip()
        context_phrases = phrases[
            phrases.str.contains(
                r"\b" + search_for + r"\b", regex=True, flags=re.IGNORECASE
            )
        ].reset_index(  # type: ignore[attr-defined]
            drop=True
        )

        return context_phrases

    # -------------------------------------------------------------------------
    def _create_contexts_dataframe(self, context_phrases: pd.Series) -> pd.DataFrame:

        pattern = self.params.pattern
        if isinstance(pattern, tuple):
            pattern = pattern[0]

        search_for = pattern.lower().replace("_", " ")

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

        return contexts.reset_index(drop=True)  # type: ignore[return-value]

    # -------------------------------------------------------------------------
    def _transform_context_dataframe_to_texts(
        self, contexts: pd.DataFrame
    ) -> list[str]:

        search_for = self.params.pattern
        if isinstance(search_for, tuple):
            search_for = search_for[0]

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

        assert self.params.source_field in [
            Field.ABSTR_RAW,
            Field.ABSTR_TOK,
            Field.ABSTR_UPPER,
        ]

        dataframe = load_filtered_main_csv_zip(params=self.params)
        context_phrases = self._extract_context_phrases(dataframe=dataframe)
        contexts_dataframe = self._create_contexts_dataframe(context_phrases)
        texts = self._transform_context_dataframe_to_texts(contexts_dataframe)

        return texts
