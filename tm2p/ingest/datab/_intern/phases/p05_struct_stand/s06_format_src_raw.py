from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s06_format_src_raw(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df[Field.SRC_RAW.value] = df[Field.SRC_RAW.value].str.upper()
    save_main_csv_zip(df, root_directory)

    return 1
