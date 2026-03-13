import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.datab._intern.oper import transform_column


def s04_extr_openalex_ctry(root_directory: str) -> int:

    ctry_to_alpha2 = load_builtin_mapping("country_to_alpha2.the.json")
    alpha2_to_ctry = {v: k for k, v in ctry_to_alpha2.items()}

    def _extract(series: pd.Series) -> pd.Series:
        series = series.str.split("; ")
        series = series.map(
            lambda x: [alpha2_to_ctry.get(i, "[n/a]") for i in x], na_action="ignore"
        )
        series = series.str.join("; ")
        return series

    return transform_column(
        source=Field.CTRY_ISO2,
        target=Field.CTRY,
        function=_extract,
        root_directory=root_directory,
    )
