# CODE_REVIEW: 2025-01-27
"""
Coalesce Column
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.data_sourc._intern.oper.coalesc_col import coalesce_column
    >>> coalesce_column(
    ...     source=Field.SRC_ISO4_RAW,
    ...     target=Field.USR0,
    ...     root_directory="tests/fintech/",
    ... )
    180

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 5;")
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...    .run()
    ... )  # doctest: +SKIP
                                                    USR0
    0  diffusion of technology; innovation in financi...
    1  fintech applications; catalysts; green finance...
    2  united arab emirates; uae; favorable attitude;...
    3  building; the information systems success mode...
    4  current study; the influence; fintech innovati...


"""


from tm2p import Field

from ._file_dispatch import get_file_operations
from .data_file import DataFile


def coalesce_column(
    source: Field,
    target: Field,
    root_directory: str,
    file: DataFile = DataFile.MAIN,
) -> int:

    assert isinstance(source, Field)
    assert isinstance(target, Field)
    assert isinstance(root_directory, str)
    assert isinstance(file, DataFile)

    load_data, save_data, get_path = get_file_operations(file)

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    if target.value in dataframe.columns:
        dataframe[target.value] = dataframe[target.value].fillna(
            dataframe[source.value]
        )
    else:
        dataframe[target.value] = dataframe[source.value]

    save_data(df=dataframe, root_directory=root_directory)

    return int(dataframe[target.value].notna().sum())
