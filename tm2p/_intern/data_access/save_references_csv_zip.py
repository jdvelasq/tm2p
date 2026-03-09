"""
Smoke test:
    >>> from tm2p._intern.data_access import save_references_csv_zip
    >>> save_references_csv_zip(params, records) # doctest: +SKIP


"""

import pandas as pd

from .get_references_csv_zip_path import get_references_csv_zip_path


def save_references_csv_zip(df: pd.DataFrame, root_directory: str) -> None:

    references_data_path = get_references_csv_zip_path(root_directory)

    temp_file = references_data_path.with_suffix(".tmp")
    df.to_csv(
        temp_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
    temp_file.replace(references_data_path)
