import pandas as pd  # type: ignore

from tm2p import Field

from ._file_dispatch import get_file_operations
from .data_file import DataFile


def merge_columns(
    sources: tuple[Field, ...],
    target: Field,
    root_directory: str,
    file: DataFile = DataFile.MAIN,
) -> int:

    load_data, save_data, _ = get_file_operations(file)

    dataframe = load_data(root_directory=root_directory, usecols=None)

    existing_sources = [col for col in sources if col.value in dataframe.columns]
    if not existing_sources:
        return 0

    all_items = None
    for source in existing_sources:
        items = dataframe[source.value].astype(str).str.split("; ")
        all_items = items if all_items is None else all_items + items

    assert all_items is not None
    all_items = all_items.apply(
        lambda x: (
            [item for item in x if item and item != "nan"]
            if isinstance(x, list)
            else []
        )
    )
    all_items = all_items.apply(lambda x: sorted(set(x)) if x else [])

    dataframe[target.value] = all_items.map(lambda x: "; ".join(x) if x else pd.NA)

    non_null_count = int(dataframe[target.value].notna().sum())

    save_data(df=dataframe, root_directory=root_directory)

    return non_null_count
