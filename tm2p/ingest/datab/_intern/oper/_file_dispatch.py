from tm2p._intern.data_access import (
    get_main_csv_zip_path,
    get_references_csv_zip_path,
    load_main_csv_zip,
    load_references_csv_zip,
    save_main_csv_zip,
    save_references_csv_zip,
)

from .data_file import DataFile


def get_file_operations(file: DataFile):
    if file == DataFile.MAIN:
        return (load_main_csv_zip, save_main_csv_zip, get_main_csv_zip_path)
    if file == DataFile.REFERENCES:
        return (
            load_references_csv_zip,
            save_references_csv_zip,
            get_references_csv_zip_path,
        )
    raise ValueError(f"Invalid file: {file}")
