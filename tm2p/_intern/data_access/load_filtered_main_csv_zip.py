"""

Smoke test:
    >>> #
    >>> # TEST PREPARATION
    >>> #
    >>> # Countries:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus, ApplyThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Organizations:
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, ApplyThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Descriptors:
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, ApplyThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> #
    >>> # CODE TESTED
    >>> #
    >>> from tm2p._internals import Params
    >>> from tm2p.database._intern.io import load_filtered_main_data
    >>> df = (
    ...     load_filtered_main_data(
    ...         Params(
    ...             database="main",
    ...             record_years_range=(None, None),
    ...             record_citations_range=(None, None),
    ...             records_order_by=None,
    ...             records_match=None,
    ...             root_directory="examples/fintech/",
    ...         )
    ...     ).head()
    ... )
    >>> assert isinstance(df, pd.DataFrame)
    >>> assert len(df) > 0
    >>> assert "year" in df.columns
    >>> df # doctest: +SKIP
                        source_title_abbr  ...  year
    0             Int. J. Appl. Eng. Res.  ...  2016
    1                   Telecommun Policy  ...  2016
    3                      China Econ. J.  ...  2016
    4  Contemp. Stud. Econ. Financ. Anal.  ...  2016
    5                    New Polit. Econ.  ...  2017
    <BLANKLINE>
    [5 rows x 80 columns]



"""

import pandas as pd  # type: ignore

from tm2p import Field, RecordsOrderBy
from tm2p._intern import Params
from tm2p._intern.data_access.load_main_csv_zip import load_main_csv_zip


def _filter_dataframe_by_year(params: Params, dataframe: pd.DataFrame) -> pd.DataFrame:

    years_range = params.record_years_range

    if years_range is None:
        return dataframe

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
        dataframe = dataframe[dataframe.year >= start_year]

    if end_year is not None:
        dataframe = dataframe[dataframe.year <= end_year]

    return dataframe


def _filter_dataframe_by_citations(
    params: Params, dataframe: pd.DataFrame
) -> pd.DataFrame:

    citations_range = params.record_citations_range

    if citations_range is None:
        return dataframe

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
        dataframe = dataframe[dataframe.global_citations >= cited_by_min]

    if cited_by_max is not None:
        dataframe = dataframe[dataframe.global_citations <= cited_by_max]

    return dataframe


def _filter_dataframe_by_match(params: Params, dataframe: pd.DataFrame) -> pd.DataFrame:

    filters = params.records_match

    if filters is None:
        return dataframe

    filters = {k.value: v for k, v in filters.items()}  # type: ignore

    for filter_name, filter_value in filters.items():

        if filter_name == Field.RID.value:

            dataframe = dataframe[dataframe[Field.RID.value].isin(filter_value)]

        else:

            # Split the filter value into a list of strings
            database = dataframe[[Field.RID.value, filter_name]].copy()
            database.loc[:, filter_name] = database[filter_name].str.split(";")

            # Explode the list of strings into multiple rows
            database = database.explode(filter_name)

            # Remove leading and trailing whitespace from the strings
            database[filter_name] = database[filter_name].str.strip()

            # Keep only records that match the filter value
            database = database[database[filter_name].isin(filter_value)]

            dataframe = dataframe[
                dataframe[Field.RID.value].isin(database[Field.RID.value])
            ]

    return dataframe


def _sort_dataframe_by(params: Params, dataframe: pd.DataFrame) -> pd.DataFrame:

    sort_by = params.records_order_by

    if sort_by is None:
        return dataframe

    if sort_by == RecordsOrderBy.YEAR_NEWEST:
        dataframe = dataframe.sort_values(
            [
                Field.YEAR.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordsOrderBy.YEAR_OLDEST:
        dataframe = dataframe.sort_values(
            [
                Field.YEAR.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )
    elif sort_by == RecordsOrderBy.GCS_BY_HIGHEST:
        dataframe = dataframe.sort_values(
            [
                Field.GCS.value,
                Field.YEAR.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordsOrderBy.GCS_BY_LOWEST:
        dataframe = dataframe.sort_values(
            [
                Field.GCS.value,
                Field.YEAR.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordsOrderBy.LCS_BY_HIGHEST:
        dataframe = dataframe.sort_values(
            [
                Field.LCS.value,
                Field.YEAR.value,
                Field.GCS.value,
            ],
            ascending=[False, False, False],
        )

    elif sort_by == RecordsOrderBy.LCS_BY_LOWEST:
        dataframe = dataframe.sort_values(
            [
                Field.LCS.value,
                Field.YEAR.value,
                Field.GCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordsOrderBy.AUTH_A_TO_Z:
        dataframe = dataframe.sort_values(
            [
                Field.AUTH_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordsOrderBy.AUTH_Z_TO_A:
        dataframe = dataframe.sort_values(
            [
                Field.AUTH_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    elif sort_by == RecordsOrderBy.SRC_A_TO_Z:
        dataframe = dataframe.sort_values(
            [
                Field.SRC_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[True, False, False],
        )

    elif sort_by == RecordsOrderBy.SRC_Z_TO_A:
        dataframe = dataframe.sort_values(
            [
                Field.SRC_NORM.value,
                Field.GCS.value,
                Field.LCS.value,
            ],
            ascending=[False, False, False],
        )
    else:
        raise ValueError(f"Unsupported sort option: {sort_by}")

    columns = sorted(dataframe.columns)
    dataframe = dataframe[columns]

    return dataframe


def load_filtered_main_csv_zip(params: Params) -> pd.DataFrame:

    dataframe = load_main_csv_zip(root_directory=params.root_directory, usecols=None)
    dataframe = _filter_dataframe_by_year(params, dataframe)
    dataframe = _filter_dataframe_by_citations(params, dataframe)
    dataframe = _filter_dataframe_by_match(params, dataframe)
    dataframe = _sort_dataframe_by(params, dataframe)

    return dataframe
