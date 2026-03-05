from pathlib import Path

import pandas as pd  # type: ignore

from tm2p.ingest.data_sourc._intern.scaffold.get_subdirectories import (
    get_subdirectories,
)


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


def compress_raw_files(root_directory: str) -> int:

    raw_dir = Path(root_directory) / "ingest" / "raw" / "scopus"

    if not raw_dir.exists():
        return 0

    files_compressed = 0
    subdirectories = get_subdirectories(raw_dir)

    for subdir in subdirectories:
        subdir_path = raw_dir / subdir
        csv_files = list(subdir_path.glob("*.csv"))

        for csv_file in csv_files:
            if _compress_file(csv_file):
                files_compressed += 1

    return files_compressed
