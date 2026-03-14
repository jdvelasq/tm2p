import pandas as pd  # type: ignore

from tm2p import Field
from tm2p.ingest.datab._intern.oper import transform_column


def s04_extr_pubmed_ctry(root_directory: str) -> int:

    def _extract(series: pd.Series) -> pd.Series:
        return series.str.split(";").str[0].str.strip()

    return transform_column(
        source=Field.AFFIL_RAW,
        target=Field.CTRY,
        function=_extract,
        root_directory=root_directory,
    )
