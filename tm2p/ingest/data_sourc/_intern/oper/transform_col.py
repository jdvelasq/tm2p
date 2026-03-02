from typing import Callable

from pandas import Series

from tm2p import Field

from ._file_dispatch import get_file_operations
from .data_file import DataFile


def transform_column(
    source: Field,
    target: Field,
    function: Callable[[Series], Series],
    root_directory: str,
    file: DataFile = DataFile.MAIN,
) -> int:

    load_data, save_data, get_path = get_file_operations(file)

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if file == DataFile.MAIN:
            raise KeyError(
                f"Source column '{source.value}' not found in {get_path(root_directory).name}"
            )

        return 0

    dataframe[target.value] = function(dataframe[source.value])

    non_null_count = int(dataframe[target.value].notna().sum())

    save_data(df=dataframe, root_directory=root_directory)

    return non_null_count
