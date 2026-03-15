# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_review_steps(params: Params) -> list[Step]:

    from .s01_extract_abstract_suffixes import s01_extract_abstract_suffixes
    from .s02_extract_section_headers import s02_extract_section_headers
    from .s03_extract_acronyms import s03_extract_acronyms

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Extracting abstract suffixes",
            function=s01_extract_abstract_suffixes,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting section headers",
            function=s02_extract_section_headers,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting acronyms",
            function=s03_extract_acronyms,
            kwargs=common_kwargs,
        ),
    ]
