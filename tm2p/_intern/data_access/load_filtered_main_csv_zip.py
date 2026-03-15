"""
Smoke test:
    >>> from tm2p._intern import Params
    >>> from tm2p._intern.data_access import load_filtered_main_csv_zip
    >>> df = (
    ...     load_filtered_main_csv_zip(
    ...         Params(
    ...             record_years_range=(None, None),
    ...             record_citations_range=(None, None),
    ...             records_order_by=None,
    ...             records_match=None,
    ...             root_directory="tests/scopus/",
    ...         )
    ...     ).head()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> assert len(df) > 0
    >>> assert "YEAR" in df.columns
    >>> df  # doctest: +NORMALIZE_WHITESPACE
                                                AUTH_RAW  ...                 USR1
    0  Wang, C.; Wang, L.; Zhao, S.; Yang, C.; Albita...  ...      BUS STRATEG ENV
    1  Hasan, F.; Al-Okaily, M.; Choudhury, T.; Kayan...  ...  ELECTRON COMMER RES
    2          Roh, T.; Yang, Y.S.; Xiao, S.; Park, B.I.  ...  ELECTRON COMMER RES
    3  Ratna, S.; Saide, S.; Putri, A.M.; Indrajit, R...  ...        EUROMED J BUS
    4                         Gao, D.; Tan, L.; Duan, K.  ...         EUR J FINANC
    <BLANKLINE>
    [5 rows x 84 columns]


    >>> df = (
    ...     load_filtered_main_csv_zip(
    ...         Params(
    ...             record_years_range=(None, None),
    ...             record_citations_range=(None, None),
    ...             records_order_by=None,
    ...             records_match=None,
    ...             root_directory="tests/scopus/",
    ...         )
    ...     ).head()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> assert len(df) > 0
    >>> assert "YEAR" in df.columns
    >>> df  # doctest: +NORMALIZE_WHITESPACE
                                                AUTH_RAW  ...                 USR1
    0  Wang, C.; Wang, L.; Zhao, S.; Yang, C.; Albita...  ...      BUS STRATEG ENV
    1  Hasan, F.; Al-Okaily, M.; Choudhury, T.; Kayan...  ...  ELECTRON COMMER RES
    2          Roh, T.; Yang, Y.S.; Xiao, S.; Park, B.I.  ...  ELECTRON COMMER RES
    3  Ratna, S.; Saide, S.; Putri, A.M.; Indrajit, R...  ...        EUROMED J BUS
    4                         Gao, D.; Tan, L.; Duan, K.  ...         EUR J FINANC
    <BLANKLINE>
    [5 rows x 84 columns]


"""

import pandas as pd  # type: ignore

from tm2p import Field, RecordOrderBy
from tm2p._intern import Params
from tm2p._intern.data_access.load_main_csv_zip import load_main_csv_zip


def _filter_dataframe_by_year(params: Params, df: pd.DataFrame) -> pd.DataFrame:

    years_range = params.record_years_range

    if years_range is None:
        return df

    if not isinstance(years_range, tuple):
        raise TypeError(
            "The record_years_range parameter must be a tuple of two values."
        )

    if len(years_range) != 2:
        raise ValueError(
            "The record_years_range parameter must be a tuple of two values."
        )

    start_year, end_year = years_range

    if start_year is not None:
        df = df.loc[df[Field.YEAR.value] >= start_year, :]

    if end_year is not None:
        df = df.loc[df[Field.YEAR.value] <= end_year, :]

    return df


def _filter_dataframe_by_citations(params: Params, df: pd.DataFrame) -> pd.DataFrame:

    citations_range = params.record_citations_range

    if citations_range is None:
        return df

    if not isinstance(citations_range, tuple):
        raise TypeError(
            "The record_citations_range parameter must be a tuple of two values."
        )

    if len(citations_range) != 2:
        raise ValueError(
            "The record_citations_range parameter must be a tuple of two values."
        )

    cited_by_min, cited_by_max = citations_range

    if cited_by_min is not None:
        df = df.loc[df[Field.GCS.value] >= cited_by_min, :]

    if cited_by_max is not None:
        df = df.loc[df[Field.GCS.value] <= cited_by_max, :]

    return df


def _filter_dataframe_by_match(params: Params, df: pd.DataFrame) -> pd.DataFrame:

    filters = params.records_match

    if filters is None:
        return df

    filtered_df = df.copy()

    for filter_name, filter_value in filters.items():

        if filter_name.value == Field.REC_ID.value:

            filtered_df = filtered_df.loc[
                filtered_df[Field.REC_ID.value].isin(filter_value), :
            ]

        else:

            # Split the filter value into a list of strings
            filtered_df = filtered_df.loc[
                :, [Field.REC_ID.value, filter_name.value]
            ].copy()
            filtered_df.loc[:, filter_name.value] = filtered_df[
                filter_name.value
            ].str.split(";")

            # Explode the list of strings into multiple rows
            filtered_df = filtered_df.explode(filter_name.value)

            # Remove leading and trailing whitespace from the strings
            filtered_df[filter_name.value] = filtered_df[filter_name.value].str.strip()

            # Keep only records that match the filter value
            filtered_df = filtered_df.loc[
                filtered_df[filter_name.value].isin(filter_value), :
            ]
            filtered_df = filtered_df.loc[
                filtered_df[Field.RID.value].isin(filtered_df[Field.RID.value]), :
            ]

    final_df = df.loc[df[Field.REC_ID.value].isin(filtered_df[Field.REC_ID.value]), :]

    return final_df


def _sort_dataframe_by(params: Params, df: pd.DataFrame) -> pd.DataFrame:

    sort_by = params.records_order_by

    if sort_by is None:
        return df

    if sort_by == RecordOrderBy.YEAR_NEWEST:
        df = df.sort_values(
            [
                Field.YEAR.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordOrderBy.YEAR_OLDEST:
        df = df.sort_values(
            [
                Field.YEAR.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )
    elif sort_by == RecordOrderBy.GCS_HIGHEST:
        df = df.sort_values(
            [
                Field.GCS.value,
                Field.YEAR.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordOrderBy.GCS_LOWEST:
        df = df.sort_values(
            [
                Field.GCS.value,
                Field.YEAR.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordOrderBy.LCS_HIGHEST:
        df = df.sort_values(
            [
                Field.LCS.value,
                Field.YEAR.value,
                Field.GCS.value,
            ],
            ascending=[False, False, False],
        )

    elif sort_by == RecordOrderBy.LCS_LOWEST:
        df = df.sort_values(
            [
                Field.LCS.value,
                Field.YEAR.value,
                Field.GCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordOrderBy.AUTH_A_TO_Z:
        df = df.sort_values(
            [
                Field.AUTH_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordOrderBy.AUTH_Z_TO_A:
        df = df.sort_values(
            [
                Field.AUTH_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordOrderBy.SRC_A_TO_Z:
        df = df.sort_values(
            [
                Field.SRC_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordOrderBy.SRC_Z_TO_A:
        df = df.sort_values(
            [
                Field.SRC_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    else:
        raise ValueError(f"Unsupported sort option: {sort_by}")

    columns = sorted(df.columns)
    df = df.loc[:, columns]

    return df


def load_filtered_main_csv_zip(params: Params) -> pd.DataFrame:

    df = load_main_csv_zip(root_directory=params.root_directory, usecols=None)
    df = _filter_dataframe_by_year(params, df)
    df = _filter_dataframe_by_citations(params, df)
    df = _filter_dataframe_by_match(params, df)
    df = _sort_dataframe_by(params, df)

    return df
