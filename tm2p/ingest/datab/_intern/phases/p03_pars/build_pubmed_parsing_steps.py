# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_pubmed_parsing_steps(params: Params) -> list[Step]:

    from .step_pubmed_to_csv import step_pubmed_to_csv

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Parsing PubMed data to CSV",
            function=step_pubmed_to_csv,
            kwargs=common_kwargs,
        ),
    ]
