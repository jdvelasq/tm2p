# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_wos_parsing_steps(params: Params) -> list[Step]:

    from .step_wos_to_csv import step_wos_to_csv

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Parsing WoS data to CSV",
            function=step_wos_to_csv,
            kwargs=common_kwargs,
        ),
    ]
