from tm2p import Field

from ._file_dispatch import get_file_operations


def rename_column(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: str = "ignore",
) -> int:

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    dataframe = dataframe.rename(columns={source.value: target.value})

    save_data(df=dataframe, root_directory=root_directory)

    return len(dataframe)
