from tm2p import Field
from tm2p.ingest.oper.transform_column import transform_column


def s10_assign_org_first(root_directory: str) -> int:

    transform_column(
        source=Field.ORG_RAW,
        target=Field.ORG_FIRST,
        function=_extract_org_first,
        root_directory=root_directory,
    )

    result = transform_column(
        source=Field.ORG_RAW,
        target=Field.ORG_RAW,
        function=_fix_org,
        root_directory=root_directory,
    )

    return result


def _extract_org_first(series):

    series = series.copy()
    series = series.str.split("; ")
    series = series.str[0]

    return series


def _fix_org(series):

    series = series.copy()
    series = series.str.split("; ")
    series = series.map(set, na_action="ignore")
    series = series.map(sorted, na_action="ignore")
    series = series.str.join("; ")

    return series
