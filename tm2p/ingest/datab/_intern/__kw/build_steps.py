# CODE_REVIEW: 2026-01-26


from tm2p import Field
from tm2p._intern import Params

from ..step import Step


def build_keyword_steps(params: Params) -> list[Step]:

    from .compose_key_norm import compose_key_norm
    from .compose_key_tok import compose_key_tok
    from .correct_hyphenated_words import correct_hyphenated_words
    from .normalize_auth_key_raw import normalize_auth_key_raw
    from .normalize_idx_key_raw import normalize_idx_key_raw
    from .tokenize_keywords import tokenize_keywords

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Tokenizing {Field.AUTHKW_RAW.value} and {Field.IDXKW_RAW.value}",
            function=tokenize_keywords,
            kwargs=common_kwargs,
            count_message="{count} records tokenized",
        ),
        Step(
            name=f"Correcting hyphenated words in {Field.AUTHKW_TOK.value} and {Field.IDXKW_TOK.value}",
            function=correct_hyphenated_words,
            kwargs=common_kwargs,
            count_message="{count} records corrected",
        ),
        Step(
            name=f"Normalizing {Field.AUTHKW_TOK.value}",
            function=normalize_auth_key_raw,
            kwargs=common_kwargs,
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Normalizing {Field.IDXKW_TOK.value}",
            function=normalize_idx_key_raw,
            kwargs=common_kwargs,
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Composing {Field.KW_TOK.value}",
            function=compose_key_tok,
            kwargs=common_kwargs,
            count_message="{count} records composed",
        ),
        Step(
            name=f"Composing {Field.KW_NORM.value}",
            function=compose_key_norm,
            kwargs=common_kwargs,
            count_message="{count} records composed",
        ),
    ]
