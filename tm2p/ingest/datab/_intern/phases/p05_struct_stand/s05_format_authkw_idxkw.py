from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s05_format_authkw_idxkw(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    if Field.AUTHKW_RAW.value in df.columns:
        col = Field.AUTHKW_RAW.value
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace("*", "", regex=False)
        save_main_csv_zip(df, root_directory)

    if Field.IDXKW_RAW.value in df.columns:
        col = Field.IDXKW_RAW.value
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace("*", "", regex=False)
        save_main_csv_zip(df, root_directory)

    return 1
