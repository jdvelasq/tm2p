# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_pubmed_filter_steps(params: Params) -> list[Step]:

    from .remov_non_english_abstr import remov_non_english_abstr

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Removing non-English abstracts from PubMed data",
            function=remov_non_english_abstr,
            kwargs=common_kwargs,
        ),
    ]
