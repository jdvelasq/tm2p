from pathlib import Path

import pandas as pd  # type: ignore

from tm2p.ingest.datab._intern.__prepare._get_subdirectories import get_subdirectories


def _compress_file(csv_file: Path) -> bool:

    try:
        zip_file = csv_file.with_suffix(".csv.zip")

        df = pd.read_csv(csv_file, encoding="utf-8", low_memory=False)
        df.to_csv(zip_file, encoding="utf-8", index=False, compression="zip")

        if zip_file.exists() and zip_file.stat().st_size > 0:
            csv_file.unlink()
            return True

        return False

    except (
        FileNotFoundError,
        PermissionError,
        OSError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        ValueError,
    ):
        return False


def _process_database(path: Path) -> int:

    if not path.exists():
        return 0

    files_compressed = 0
    subdirectories = get_subdirectories(path)

    for subdir in subdirectories:
        subdir_path = path / subdir
        csv_files = list(subdir_path.glob("*.csv"))

        for csv_file in csv_files:
            if _compress_file(csv_file):
                files_compressed += 1

    return files_compressed


def compress_raw_files(root_directory: str) -> int:

    openalex_path = Path(root_directory) / "ingest" / "raw" / "openalex"
    scopus_path = Path(root_directory) / "ingest" / "raw" / "scopus"
    wos_path = Path(root_directory) / "ingest" / "raw" / "wos"

    processed = 0
    processed += _process_database(openalex_path)
    processed += _process_database(scopus_path)
    processed += _process_database(wos_path)

    return processed
