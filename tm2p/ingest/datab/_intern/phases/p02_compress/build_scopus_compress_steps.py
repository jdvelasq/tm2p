# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_scopus_compress_steps(params: Params) -> list[Step]:

    from .build_openalex_compress_steps import _compress_files

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Compressing Scopus raw data",
            function=_compress_files,
            kwargs=common_kwargs,
        ),
    ]
