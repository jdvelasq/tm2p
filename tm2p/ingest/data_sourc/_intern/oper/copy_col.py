# CODE_REVIEW: 2025-01-27
"""
Copy Column
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.data_sourc._intern.oper.copy_col import copy_column
    >>> copy_column(
    ...     source=Field.SRC_ISO4_RAW,
    ...     target=Field.USR0,
    ...     root_directory="tests/scopus/",
    ... )
    180

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 5;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...    .run()
    ... )
                                                    USR0
    0                           J. Financ. Rep. Account.
    1  Harnessing Blockchain-Digit. Twin Fusion for S...
    2                           J. Financ. Rep. Account.
    3                             Electron. Commer. Res.
    4                            Int. Rev. Econ. Financ.


"""

from tm2p import Field

from ._file_dispatch import get_file_operations
from .data_file import DataFile


def copy_column(
    source: Field,
    target: Field,
    root_directory: str,
    file: DataFile = DataFile.MAIN,
) -> int:

    load_data, save_data, get_path = get_file_operations(file)

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    dataframe[target.value] = dataframe[source.value]

    save_data(df=dataframe, root_directory=root_directory)

    return int(dataframe[target.value].notna().sum())
