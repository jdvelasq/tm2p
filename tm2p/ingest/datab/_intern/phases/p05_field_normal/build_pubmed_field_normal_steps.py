# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_pubmed_field_normal_steps(params: Params) -> list[Step]:

    from .normal_pubmed_raw_auth import normal_pubmed_raw_auth

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Normalizeing AUTH_RAW",
            function=normal_pubmed_raw_auth,
            kwargs=common_kwargs,
        ),
    ]
