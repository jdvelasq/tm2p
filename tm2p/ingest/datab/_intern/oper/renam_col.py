from tm2p import Field

from ._file_dispatch import get_file_operations
from .data_file import DataFile


def rename_column(
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

    dataframe = dataframe.rename(columns={source.value: target.value})

    save_data(df=dataframe, root_directory=root_directory)

    return len(dataframe)
