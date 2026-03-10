"""
Smoke test:
    >>> from tm2p._intern.data_access import load_main_csv_zip
    >>> df = load_main_csv_zip(root_directory="tests/scopus/")
    >>> type(df).__name__
    'DataFrame'

    >>> df = load_main_csv_zip(
    ...     root_directory="tests/scopus/",
    ...     usecols=["RID", "TITLE_RAW"],
    ... )
    >>> type(df).__name__
    'DataFrame'



"""

from typing import Optional

import pandas as pd  # type: ignore

from .get_main_csv_zip_path import get_main_csv_zip_path


def load_main_csv_zip(
    root_directory: str,
    usecols: Optional[list[str]] = None,
) -> pd.DataFrame:

    path = get_main_csv_zip_path(root_directory)

    if not path.exists():
        raise AssertionError(f"{path.name} not found")

    try:
        return pd.read_csv(
            path,
            usecols=usecols,
            compression="zip",
            encoding="utf-8",
            low_memory=False,
        )
    except ValueError as err:
        raise AssertionError(f'Columns "{usecols}" not found in {path.name}') from err
