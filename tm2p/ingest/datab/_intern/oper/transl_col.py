from typing import Optional

from tm2p import Field
from tm2p._intern.packag_data import load_builtin_mapping

from ._file_dispatch import get_file_operations


def rename_column(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: Optional[str] = None,
) -> int:

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    british_to_american = load_builtin_mapping("british_to_american.json")
    for british, american in british_to_american.items():
        american_value = american[0] if isinstance(american, list) else american
        dataframe[target.value] = dataframe[source.value].str.replace(
            british, american_value, regex=False
        )

    save_data(df=dataframe, root_directory=root_directory)

    return len(dataframe)
