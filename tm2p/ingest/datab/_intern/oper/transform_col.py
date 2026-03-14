from typing import Callable

from pandas import Series  # type: ignore

from tm2p import Field

from ._file_dispatch import get_file_operations


def transform_column(
    source: Field,
    target: Field,
    function: Callable[[Series], Series],
    root_directory: str,
    na_action: str = "ignore",
) -> int:

    load_data, save_data, get_path = get_file_operations()

    df = load_data(root_directory=root_directory, usecols=None)

    if source.value not in df.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    df[target.value] = function(df[source.value])

    non_null_count = int(df[target.value].notna().sum())

    save_data(df=df, root_directory=root_directory)

    return non_null_count
