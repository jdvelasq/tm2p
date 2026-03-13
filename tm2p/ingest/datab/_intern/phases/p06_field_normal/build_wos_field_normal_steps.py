# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_wos_field_normal_steps(params: Params) -> list[Step]:

    from .normal_wos_auth_raw import normalize_auth_raw
    from .repair_gcs import repair_gcs

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Renaming WoS columns",
            function=normalize_auth_raw,
            kwargs=common_kwargs,
        ),
        Step(
            name="Repairing GCS",
            function=repair_gcs,
            kwargs=common_kwargs,
        ),
    ]
