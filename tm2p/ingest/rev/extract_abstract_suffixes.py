"""
ExtractAbstractSuffixes
===============================================================================

Smoke test:
    >>> from tm2p.ingest.rev import ExtractAbstractSuffixes
    >>> text = (
    ...     ExtractAbstractSuffixes()
    ...     .having_n_chars(90)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    >>> assert isinstance(text, list)
    >>> assert all(isinstance(t, str) for t in text)
    >>> assert all(len(t) <= 90 for t in text)
    >>> assert len(text) > 0
    >>> for t in text[:10]: print(t)
    TION may have for THE_FUTURE_LANDSCAPE of FINANCIAL_INTERMEDIATION . 2021 the author ( s )
    NVIRONMENTAL_PROTECTION_INITIATIVES that promote GREEN_CONSUMPTION . 2021 the author ( s )
    or FUTURE_FINTECH_RESEARCH while anticipating THE_CHALLENGES ahead . 2022 the author ( s )
    complement OTHER_FORMS of CREDIT , rather than substitute for them . 2022 the author ( s )
    FINTECH_SERVICES in advancing THE_HORIZON of THE_EXTANT_LITERATURE . 2023 the author ( s )
    at FINTECH is AN_APPROPRIATE_NEW_TECHNOLOGY for FINANCIAL_SERVICES . 2024 the author ( s )
    ften build PRODUCT_RELATED_COLLABORATIONS with LARGER_FINTECHS . 2020 , the author ( s ) .
    NTS in MONEY transferring SYSTEMS could help to decrease COSTS . 2021 , the author ( s ) .
    ORK for BALANCED_FINTECH_SECTOR_GROWTH in DEVELOPING_COUNTRIES . 2022 , the author ( s ) .
    TORS , REGULATORS , etc . ) , who explore THE_FIELD of FINTECH . 2016 , the author ( s ) .


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.rec.record_mapping import RecordMapping  # type: ignore

__reviewed__ = "2026-01-28"


class ExtractAbstractSuffixes(
    ParamsMixin,
):
    """:meta private:"""

    def _sort_by_suffix(self, texts: list[str]) -> list[str]:
        reversed_texts = [text[::-1] for text in texts]
        sorted_reversed = sorted(reversed_texts)
        return [text[::-1] for text in sorted_reversed]

    def run(self) -> list[str]:

        docs = RecordMapping().update(**self.params.__dict__).run()

        abstracts = [doc["AB"] for doc in docs if isinstance(doc["AB"], str)]
        suffixes = [text[-self.params.n_chars :] for text in abstracts]

        suffixes_grouped_by_ending = self._sort_by_suffix(suffixes)

        if self.params.pattern is not None:
            suffixes_grouped_by_ending = [
                text
                for text in suffixes_grouped_by_ending
                if self.params.pattern in text  # type: ignore
            ]

        return suffixes_grouped_by_ending
