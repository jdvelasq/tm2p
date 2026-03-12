# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_scaffolding_steps(params: Params) -> list[Step]:

    from .create_project_structure import create_project_structure

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Creating project structure",
            function=create_project_structure,
            kwargs=common_kwargs,
        ),
    ]
