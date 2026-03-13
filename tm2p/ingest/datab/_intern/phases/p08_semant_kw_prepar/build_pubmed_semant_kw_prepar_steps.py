# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_pubmed_semant_keyword_prepar_steps(params: Params) -> list[Step]:

    from .s01_token_kw import s01_token_keywordtoken_keyword

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Tokenizing keywords",
            function=s01_token_keywordtoken_keyword,
            kwargs=common_kwargs,
        ),
    ]
