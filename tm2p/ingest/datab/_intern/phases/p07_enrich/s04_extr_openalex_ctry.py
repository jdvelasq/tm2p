import pandas as pd  # type: ignore

from tm2p import Field
from tm2p.ingest.datab._intern.oper import transform_column


def s04_extr_openalex_ctry(root_directory: str) -> int:

    def _extract(series: pd.Series) -> pd.Series:
        return series.str.split(";").str[0].str.strip()

    return transform_column(
        source=Field.AUTH_NORM,
        target=Field.AUTH_FIRST,
        function=_extract,
        root_directory=root_directory,
    )
