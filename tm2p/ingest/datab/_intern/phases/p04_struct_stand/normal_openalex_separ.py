from pathlib import Path

import pandas as pd  # type: ignore


def normal_openalex_separ(root_directory: str) -> int:

    filepath = Path(root_directory) / "ingest" / "process" / "main.csv.zip"

    if not filepath.exists():
        return 0

    df = pd.read_csv(
        str(filepath), encoding="utf-8", compression="zip", low_memory=False
    )

    df = df.replace(r"\|", "; ", regex=True)

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
