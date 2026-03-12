from pathlib import Path

import pandas as pd  # type: ignore


def step_scopus_to_csv(root_directory: str) -> int:
    """:meta private:"""

    main_filepath = Path(root_directory) / "ingest" / "raw" / "main"
    ref_filepath = Path(root_directory) / "ingest" / "raw" / "ref"

    main_csv_files = list(main_filepath.glob("*.csv"))
    ref_csv_files = list(ref_filepath.glob("*.csv"))

    _generate_csv_zip_file(root_directory, main_csv_files, "main.csv.zip")
    _generate_csv_zip_file(root_directory, ref_csv_files, "ref.csv.zip")

    _compress_original_files(main_csv_files)
    _compress_original_files(ref_csv_files)

    return len(main_csv_files) + len(ref_csv_files)


def _compress_original_files(csv_files):
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df.to_csv(csv_file + ".zip", index=False, compression="zip")
        csv_file.unlink()


def _generate_csv_zip_file(root_directory, csv_files, filename):

    dfs = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8", low_memory=False)
        dfs.append(df)
    concatenated_df = pd.concat(dfs, ignore_index=True)

    filepath = Path(root_directory) / "ingest" / "processed" / filename

    concatenated_df.to_csv(
        filepath,
        index=False,
        encoding="utf-8",
        compression="zip",
    )
