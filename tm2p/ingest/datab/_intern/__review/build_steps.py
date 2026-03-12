# CODE_REVIEW: 2026-02-10


from tm2p._intern import Params

from ..step import Step


def build_review_steps(params: Params) -> list[Step]:

    from .extract_abstract_suffixes import extract_abstract_suffixes
    from .extract_acronyms import extract_acronyms
    from .extract_section_headers import extract_section_headers

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Extracting copyright text",
            function=extract_abstract_suffixes,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
        Step(
            name="Extracting section headers",
            function=extract_section_headers,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
        Step(
            name="Extracting acronyms",
            function=extract_acronyms,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
    ]
