# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_pubmed_struct_stand_steps(params: Params) -> list[Step]:

    from .drop_empty_col import drop_empty_col
    from .renam_pubmed_col import renam_pubmed_col

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Renaming PubMed columns",
            function=renam_pubmed_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Dropping empty columns",
            function=drop_empty_col,
            kwargs=common_kwargs,
        ),
    ]
