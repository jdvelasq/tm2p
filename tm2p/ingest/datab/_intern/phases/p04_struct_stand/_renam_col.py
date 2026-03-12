from pathlib import Path

import pandas as pd  # type: ignore


def renam_col(filepath: Path, names_to_tm2: dict[str, str]) -> int:

    if not filepath.exists():
        return 0

    df = pd.read_csv(
        str(filepath),
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    df.rename(columns=names_to_tm2, inplace=True)
    df = df.reindex(columns=sorted(df.columns))

    temp_file = filepath.with_suffix(".tmp")
    df.to_csv(
        temp_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
    temp_file.replace(filepath)

    return 1
