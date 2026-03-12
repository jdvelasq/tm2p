# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_openalex_struct_stand_steps(params: Params) -> list[Step]:

    from .drop_empty_col import drop_empty_col
    from .normal_openalex_separ import normal_openalex_separ
    from .renam_openalex_col import renam_openalex_col

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Renaming OpenAlex columns",
            function=renam_openalex_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Dropping empty columns",
            function=drop_empty_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Normalizing item separators",
            function=normal_openalex_separ,
            kwargs=common_kwargs,
        ),
    ]
