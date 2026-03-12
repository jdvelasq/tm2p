from pathlib import Path

import pandas as pd  # type: ignore


def create_database_files(root_directory: str) -> dict[str, int]:

    raw_directory = Path(root_directory) / "ingest" / "raw" / "scopus"
    processed_directory = Path(root_directory) / "ingest" / "process"

    if not raw_directory.exists():
        return {}

    record_counts = {}

    for subdir in ["main", "references"]:

        subdir_path = raw_directory / subdir

        if not subdir_path.exists():
            record_counts[subdir] = 0
            continue

        zip_files = list(subdir_path.glob("*.zip"))

        if not zip_files:
            record_counts[subdir] = 0
            continue

        # Read and concatenate all ZIP files
        data_frames = []
        for zip_file in zip_files:
            df = pd.read_csv(
                zip_file,
                sep=",",
                encoding="utf-8",
                index_col=False,
                on_bad_lines="skip",
                low_memory=False,
            )
            data_frames.append(df)

        # Concatenate, remove duplicates, sort
        concatenated_df = pd.concat(data_frames, ignore_index=True).drop_duplicates()
        sorted_df = concatenated_df.sort_values(
            by=["Year", "Source title", "Title"], ascending=[False, True, True]
        )

        # Save processed file
        output_path = processed_directory / f"{subdir}.csv.zip"
        sorted_df.to_csv(
            output_path,
            sep=",",
            encoding="utf-8",
            index=False,
            compression="zip",
        )

        record_counts[subdir] = len(sorted_df)

    return record_counts
