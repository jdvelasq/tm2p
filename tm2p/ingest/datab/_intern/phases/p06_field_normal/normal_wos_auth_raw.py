from tm2p.enum import Field

from ...oper.transform_col import transform_column


def normalize_auth_raw(root_directory: str) -> int:

    def _normalize_row(series):
        series = series.copy()
        series = series.str.replace(".", "", regex=False)
        series = series.str.replace(",", "", regex=False)
        return series

    return transform_column(
        source=Field.AUTH_RAW,
        target=Field.AUTH_RAW,
        function=_normalize_row,
        root_directory=root_directory,
    )
