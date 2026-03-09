"""

Smoke test:
    >>> from tm2p._intern.data_access import get_main_csv_zip_path
    >>> get_main_csv_zip_path("my_root_directory")
    PosixPath('my_root_directory/ingest/processed/main.csv.zip')


"""

from pathlib import Path


def get_main_csv_zip_path(root_directory: str) -> Path:

    return Path(root_directory) / "ingest" / "processed" / "main.csv.zip"
