# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ..oper import DataFile
from ..step import Step


def build_author_steps(params: Params) -> list[Step]:

    from .calculate_numauth import calculate_numauth
    from .disambiguate_auth_norm import disambiguate_auth_norm
    from .normalize_auth_id_raw import normalize_auth_id_raw
    from .normalize_auth_raw import normalize_auth_raw

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Normalizing '{Field.AUTHID_RAW.value}' in main.csv.zip",
            function=normalize_auth_id_raw,
            kwargs={
                "root_directory": params.root_directory,
                "file": DataFile.MAIN,
            },
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Normalizing '{Field.AUTHID_RAW.value}' in references.csv.zip",
            function=normalize_auth_id_raw,
            kwargs={
                "root_directory": params.root_directory,
                "file": DataFile.REFERENCES,
            },
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Normalizing '{Field.AUTH_RAW.value}' in main.csv.zip",
            function=normalize_auth_raw,
            kwargs={
                "root_directory": params.root_directory,
                "file": DataFile.MAIN,
            },
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Normalizing '{Field.AUTH_RAW.value}' in references.csv.zip",
            function=normalize_auth_raw,
            kwargs={
                "root_directory": params.root_directory,
                "file": DataFile.REFERENCES,
            },
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Disambiguating '{Field.AUTH_NORM.value}'",
            function=disambiguate_auth_norm,
            kwargs=common_kwargs,
            count_message="{count} records disambiguated",
        ),
        Step(
            name=f"Calculating '{Field.N_AUTH.value}'",
            function=calculate_numauth,
            kwargs=common_kwargs,
            count_message="{count} records calculated",
        ),
    ]
