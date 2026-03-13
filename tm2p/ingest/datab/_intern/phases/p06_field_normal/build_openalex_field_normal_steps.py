# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_openalex_field_normal_steps(params: Params) -> list[Step]:

    from .s01_normal_openalex_auth_raw import s01_normal_openalex_auth_raw
    from .s02_repair_openalex_authid import s02_repair_openalex_authid
    from .s03_disambig_auth_norm import s03_disambig_auth_norm
    from .s04_repair_gcs import s04_repair_gcs

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Normalizing AUTH_RAW",
            function=s01_normal_openalex_auth_raw,
            kwargs=common_kwargs,
        ),
        Step(
            name="Repairing AUTHID",
            function=s02_repair_openalex_authid,
            kwargs=common_kwargs,
        ),
        Step(
            name="Disambiguating AUTH_NORM",
            function=s03_disambig_auth_norm,
            kwargs=common_kwargs,
        ),
        Step(
            name="Repairing GCS",
            function=s04_repair_gcs,
            kwargs=common_kwargs,
        ),
    ]
