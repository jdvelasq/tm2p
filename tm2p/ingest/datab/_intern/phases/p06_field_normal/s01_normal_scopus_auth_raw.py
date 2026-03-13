import pandas as pd  # type: ignore

from tm2p.enum import Field

from ...oper.transform_col import transform_column


def s01_normal_scopus_auth_raw(root_directory: str) -> int:

    def _normalize(series):
        series = series.copy()
        series = series.str.replace(r", \(\d\)", "", regex=True)
        series = series.str.replace(",", "", regex=False)
        series = series.str.replace("; ", ";", regex=False)
        series = series.str.replace(";", "; ", regex=False)
        series = series.str.replace(" Jr.", ", Jr.", regex=False)

        series = series.str.title()
        series = series.fillna(pd.NA)
        series = series.map(
            lambda x: (
                pd.NA
                if isinstance(x, str) and x.startswith("[") and x.endswith("]")
                else x
            )
        )
        series = series.map(
            lambda x: pd.NA if isinstance(x, str) and x.lower() == "anonymous" else x
        )
        series = series.map(
            lambda x: pd.NA if isinstance(x, str) and x.lower() == "anon" else x
        )
        return series

    return transform_column(
        source=Field.AUTH_RAW,
        target=Field.AUTH_RAW,
        function=_normalize,
        root_directory=root_directory,
    )


def _normalize_authid_raw(root_directory: str) -> int:

    def _normalize(series: pd.Series) -> pd.Series:

        series = series.astype("string")
        mask = series.eq("1") | (series.str.startswith("[") & series.str.endswith("]"))
        series = series.mask(mask.fillna(False), pd.NA)

        series = series.str.replace(r";$", "", regex=True)
        return series

    return transform_column(
        source=Field.AUTHID_RAW,
        target=Field.AUTHID_NORM,
        function=_normalize,
        root_directory=root_directory,
    )
