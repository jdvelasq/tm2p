"""
Smoke test:
    >>> from tm2p._intern.data_access import save_main_csv_zip
    >>> save_main_csv_zip(params, records) # doctest: +SKIP


"""

import pandas as pd

from tm2p._intern.data_access.get_main_csv_zip_path import get_main_csv_zip_path


def save_main_csv_zip(df: pd.DataFrame, root_directory: str) -> None:

    df = df.reindex(sorted(df.columns), axis=1)

    main_data_path = get_main_csv_zip_path(root_directory)
    temp_file = main_data_path.with_suffix(".tmp")
    df.to_csv(
        temp_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
    temp_file.replace(main_data_path)
