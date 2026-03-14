# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_nlp_prepar_steps(params: Params) -> list[Step]:

    from .s01_tokenize_raw_abstract import s01_tokenize_raw_abstract
    from .s02_tokenize_raw_title import s02_tokenize_raw_title
    from .s03_extract_textblob_phrases import s03_extract_textblob_phrases
    from .s04_extract_spacy_phrases import s04_extract_spacy_phrases
    from .s05_extract_abstract_acronyms import s05_extract_abstract_acronyms
    from .s06_uppercase_abstract_phrases import s06_uppercase_abstract_phrases
    from .s07_uppercase_title_phrases import s07_uppercase_title_phrases
    from .s08_extract_abstract_phrases import s08_extract_abstract_phrases
    from .s09_extract_title_phrases import s09_extract_title_phrases
    from .s10_merge_title_and_abstract_phrases import (
        s10_merge_title_and_abstract_phrases,
    )

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Tokenizing ABTR",
            function=s01_tokenize_raw_abstract,
            kwargs=common_kwargs,
        ),
        Step(
            name="Tokenizing TITLE",
            function=s02_tokenize_raw_title,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting TextBlob phrases",
            function=s03_extract_textblob_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting spaCy phrases",
            function=s04_extract_spacy_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting abstract acronyms",
            function=s05_extract_abstract_acronyms,
            kwargs=common_kwargs,
        ),
        Step(
            name="Uppercasing ABSTR",
            function=s06_uppercase_abstract_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Uppercasing TITLE",
            function=s07_uppercase_title_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting ABSTR phrases",
            function=s08_extract_abstract_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting TITLE phrases",
            function=s09_extract_title_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Merging TITLE and ABSTR phrases",
            function=s10_merge_title_and_abstract_phrases,
            kwargs=common_kwargs,
        ),
    ]
