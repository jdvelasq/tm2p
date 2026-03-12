from pathlib import Path

import pandas as pd  # type: ignore


def drop_empty_columns(root_directory: str) -> dict[str, list[str]]:

    processed_dir = Path(root_directory) / "ingest" / "process"

    files_to_process = {
        "main": processed_dir / "main.csv.zip",
        "references": processed_dir / "references.csv.zip",
    }

    dropped_columns: dict[str, list[str]] = {}

    for file_type, file_path in files_to_process.items():

        if not file_path.exists():
            dropped_columns[file_type] = []
            continue

        data_frame = pd.read_csv(
            file_path,
            encoding="utf-8",
            compression="zip",
            low_memory=False,
        )

        original_cols = set(data_frame.columns)

        data_frame = data_frame.dropna(axis=1, how="all")

        remaining_cols = set(data_frame.columns)
        removed = sorted(original_cols - remaining_cols)
        dropped_columns[file_type] = removed

        if removed:
            data_frame.to_csv(
                file_path,
                sep=",",
                encoding="utf-8",
                index=False,
                compression="zip",
            )

    return dropped_columns
