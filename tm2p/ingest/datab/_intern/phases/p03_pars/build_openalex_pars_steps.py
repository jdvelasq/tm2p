# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_openalex_pars_steps(params: Params) -> list[Step]:

    from .step_openalex_to_csv import step_openalex_to_csv

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Parsing OpenAlex data to CSV",
            function=step_openalex_to_csv,
            kwargs=common_kwargs,
        ),
    ]
