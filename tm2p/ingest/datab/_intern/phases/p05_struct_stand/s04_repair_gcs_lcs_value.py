from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s04_repair_gcs_lcs_value(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    for field in (Field.GCS, Field.LCS):
        if field.value not in df.columns:
            df[field.value] = 0
        df[field.value] = df[field.value].fillna(0).astype(int)

    save_main_csv_zip(df, root_directory)

    return 1
