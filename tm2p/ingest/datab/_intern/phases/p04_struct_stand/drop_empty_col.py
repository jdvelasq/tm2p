from pathlib import Path

import pandas as pd  # type: ignore


def drop_empty_col(root_directory: str) -> int:

    main_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"

    df = pd.read_csv(
        str(main_file),
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    n_before = len(df.columns)

    df.dropna(axis=1, how="all", inplace=True)

    n_after = len(df.columns)

    temp_file = main_file.with_suffix(".tmp")
    df.to_csv(
        temp_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
    temp_file.replace(main_file)

    return n_before - n_after
