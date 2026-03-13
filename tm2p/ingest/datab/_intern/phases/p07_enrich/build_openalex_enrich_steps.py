# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_openalex_enrich_steps(params: Params) -> list[Step]:

    from .s01_calcul_n_auth import s01_calcul_n_auth
    from .s02_create_auth_first import s02_create_auth_first
    from .s03_calcul_openalex_n_gcr import s03_calcul_openalex_n_gcr
    from .s04_extr_openalex_ctry import s04_extr_openalex_ctry
    from .s05_assign_ctry_first import assign_ctry_first
    from .s06_assign_region import s06_assign_region
    from .s07_assign_subregion import s07_assign_subregion
    from .s08_assign_ctry_iso3 import s08_assign_ctry_iso3
    from .s09_extr_openalex_org import s09_extr_openalex_org
    from .s10_assign_org_first import s10_assign_org_first

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
            function=s03_calcul_openalex_n_gcr,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting CTRY",
            function=s04_extr_openalex_ctry,
            kwargs=common_kwargs,
        ),
        Step(
            name="Assigning CTRY_FIRST",
            function=assign_ctry_first,
            kwargs=common_kwargs,
        ),
        Step(
            name="Assigning REGION",
            function=s06_assign_region,
            kwargs=common_kwargs,
        ),
        Step(
            name="Assigning SUBREGION",
            function=s07_assign_subregion,
            kwargs=common_kwargs,
        ),
        Step(
            name="Assigning CTRY_ISO3",
            function=s08_assign_ctry_iso3,
            kwargs=common_kwargs,
        ),
        Step(
            name="Extracting ORG",
            function=s09_extr_openalex_org,
            kwargs=common_kwargs,
        ),
        Step(
            name="Assigning ORG_FIRST",
            function=s10_assign_org_first,
            kwargs=common_kwargs,
        ),
    ]
