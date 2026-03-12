# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_scopus_struct_stand_steps(params: Params) -> list[Step]:

    from .drop_empty_col import drop_empty_col
    from .renam_scopus_col import renam_scopus_col

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Renaming Scopus columns",
            function=renam_scopus_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Dropping empty columns",
            function=drop_empty_col,
            kwargs=common_kwargs,
        ),
    ]
