# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_wos_enrich_steps(params: Params) -> list[Step]:

    from .s01_calcul_n_auth import s01_calcul_n_auth
    from .s02_create_auth_first import s02_create_auth_first
    from .s03_calcul_wos_n_gcr import s03_calcul_wos_n_gcr

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Calulating N_AUTH",
            function=s01_calcul_n_auth,
            kwargs=common_kwargs,
        ),
        Step(
            name="Creating AUTH_FIRST",
            function=s02_create_auth_first,
            kwargs=common_kwargs,
        ),
        Step(
            name="Calculating N_GCR",
            function=s03_calcul_wos_n_gcr,
            kwargs=common_kwargs,
        ),
    ]
