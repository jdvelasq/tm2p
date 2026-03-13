# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ...step import Step


def build_openalex_semant_keyword_prepar_steps(params: Params) -> list[Step]:

    from .s01_token_kw import s01_token_keywordtoken_keyword
    from .s02_correct_hyphen_word import s02_correct_hyphen_word
    from .s03_normal_auth_idx_kw_tok import s03_normal_auth_idx_key_tok
    from .s04_compose_kw_tok import s04_compose_kw_tok
    from .s05_compose_key_norm import s05_compose_key_norm

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Tokenizing keywords",
            function=s01_token_keywordtoken_keyword,
            kwargs=common_kwargs,
        ),
        Step(
            name="Correcting hyphenated words",
            function=s02_correct_hyphen_word,
            kwargs=common_kwargs,
        ),
        Step(
            name=f"Normalizing {Field.AUTHKW_TOK.value} and {Field.IDXKW_TOK.value}",
            function=s03_normal_auth_idx_key_tok,
            kwargs=common_kwargs,
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Composing {Field.KW_TOK.value}",
            function=s04_compose_kw_tok,
            kwargs=common_kwargs,
            count_message="{count} records composed",
        ),
        Step(
            name=f"Composing {Field.KW_NORM.value}",
            function=s05_compose_key_norm,
            kwargs=common_kwargs,
            count_message="{count} records composed",
        ),
    ]
