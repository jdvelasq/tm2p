from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field


def assign_recno(root_directory):

    database_file = Path(root_directory) / "ingest" / "processed" / "main.csv.zip"

    if not database_file.exists():
        raise AssertionError(f"{database_file.name} not found")

    dataframe = pd.read_csv(
        database_file,
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    num_zeros = len(str(len(dataframe)))
    dataframe[Field.RNO.value] = [
        f"{i:0{num_zeros}d}" for i in range(1, len(dataframe) + 1)
    ]

    dataframe.to_csv(
        database_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
