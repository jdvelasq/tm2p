# CODE_REVIEW: 2025-01-27
"""
Count Column Items
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.data_sourc._intern.oper.count_col_item import count_column_items
    >>> count_column_items(
    ...     source=Field.AUTH_RAW,
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
    0     1
    1     2
    2     4
    3     4
    4     5


"""

from typing import Optional

from tm2p import Field

from ._file_dispatch import get_file_operations


def count_column_items(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: Optional[str] = None,
) -> int:

    assert isinstance(source, Field)
    assert isinstance(target, Field)

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    dataframe[target.value] = (
        dataframe[source.value].str.split("; ").str.len().fillna(0).astype(int)
    )

    save_data(df=dataframe, root_directory=root_directory)

    return int(len(dataframe))
