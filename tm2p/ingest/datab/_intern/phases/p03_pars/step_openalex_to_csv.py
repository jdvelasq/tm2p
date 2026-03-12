from pathlib import Path

import pandas as pd  # type: ignore


def step_openalex_to_csv(root_directory: str) -> int:
    """:meta private:"""

    filepath = Path(root_directory) / "ingest" / "raw"
    zip_files = list(filepath.glob("*.zip"))

    _generate_main_csv_zip_file(root_directory, zip_files)

    return len(zip_files)


def _generate_main_csv_zip_file(root_directory, zip_files):

    dfs = []

    for zip_file in zip_files:
        df = pd.read_csv(
            zip_file, encoding="utf-8", low_memory=False, compression="zip"
        )
        dfs.append(df)

    if not dfs:
        return

    concat_df = pd.concat(dfs, ignore_index=True)
    concat_df = concat_df.drop_duplicates()
    main_path = Path(root_directory) / "ingest" / "process" / "main.csv.zip"
    concat_df.to_csv(str(main_path), index=False, encoding="utf-8", compression="zip")
