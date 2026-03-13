from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s04_set_gcs_value(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    if Field.GCS.value not in df.columns:
        df[Field.GCS.value] = 0
    df[Field.GCS.value] = df[Field.GCS.value].fillna(0).astype(int)
    save_main_csv_zip(df, root_directory)

    return 1
