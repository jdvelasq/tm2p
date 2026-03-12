from functools import lru_cache
from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.packag_data import load_builtin_csv


@lru_cache(maxsize=1)
def _load_subject_areas() -> pd.DataFrame:
    return load_builtin_csv(filename="subject_areas.csv")


def assign_subjarea(root_directory: str) -> int:

    database_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"

    if not database_file.exists():
        raise AssertionError(f"{database_file.name} not found")

    dataframe = pd.read_csv(
        database_file,
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    if (
        Field.ISSN.value not in dataframe.columns
        and Field.ISSNE.value not in dataframe.columns
    ):
        return 0

    subject_areas_df = _load_subject_areas()

    issn_mapping = dict(
        zip(
            subject_areas_df[Field.ISSN.value].dropna(),
            subject_areas_df[Field.ASJC.value].dropna(),
        )
    )
    eissn_mapping = dict(
        zip(
            subject_areas_df[Field.ISSNE.value].dropna(),
            subject_areas_df[Field.ASJC.value].dropna(),
        )
    )

    dataframe[Field.ASJC.value] = None

    if Field.ISSN.value in dataframe.columns:
        dataframe[Field.ASJC.value] = dataframe[Field.ISSN.value].map(issn_mapping)

    if Field.ISSNE.value in dataframe.columns:
        dataframe[Field.ASJC.value] = dataframe[Field.ASJC.value].fillna(
            dataframe[Field.ISSNE.value].map(eissn_mapping)
        )

    non_null_count = int(dataframe[Field.ASJC.value].notna().sum())

    temp_file = database_file.with_suffix(".tmp")
    dataframe.to_csv(
        temp_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )
    temp_file.replace(database_file)

    return non_null_count
