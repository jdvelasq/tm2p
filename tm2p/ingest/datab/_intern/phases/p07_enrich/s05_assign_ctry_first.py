from tm2p import Field
from tm2p.ingest.oper.transform_column import transform_column


def assign_ctry_first(root_directory: str) -> int:

    transform_column(
        source=Field.CTRY,
        target=Field.CTRY_FIRST,
        function=_extract_ctry_first,
        root_directory=root_directory,
    )

    result = transform_column(
        source=Field.CTRY,
        target=Field.CTRY,
        function=_fix_ctry,
        root_directory=root_directory,
    )

    return result


def _extract_ctry_first(series):

    series = series.copy()
    series = series.str.split("; ")
    series = series.str[0]

    return series


def _fix_ctry(series):

    series = series.copy()
    series = series.str.split("; ")
    series = series.map(set, na_action="ignore")
    series = series.map(sorted, na_action="ignore")
    series = series.str.join("; ")

    return series
