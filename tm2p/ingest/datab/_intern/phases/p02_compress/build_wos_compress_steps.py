# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_wos_compress_steps(params: Params) -> list[Step]:

    from .build_pubmed_compress_steps import _compress_files

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Compressing WoS raw data",
            function=_compress_files,
            kwargs=common_kwargs,
        ),
    ]
