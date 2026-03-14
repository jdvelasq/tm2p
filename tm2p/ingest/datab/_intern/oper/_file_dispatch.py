from tm2p._intern.data_access import (
    get_main_csv_zip_path,
    load_main_csv_zip,
    save_main_csv_zip,
)


def get_file_operations():

    return (load_main_csv_zip, save_main_csv_zip, get_main_csv_zip_path)
