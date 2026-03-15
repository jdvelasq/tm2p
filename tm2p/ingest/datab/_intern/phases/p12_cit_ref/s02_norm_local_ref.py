import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip

REC_ID = Field.REC_ID.value
GCR_NORM = Field.GCR_WOS_FORMAT.value
LCR_NORM = Field.LCR_NORM.value


def s02_norm_local_ref(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory=root_directory)
    main_rid = df[REC_ID].dropna().drop_duplicates().to_list()

    if GCR_NORM not in df.columns:
        return 0

    def extract(row):
        if pd.isna(row[GCR_NORM]):
            return pd.NA
        gcr = row[GCR_NORM]
        gcr = gcr.split("; ")
        gcr = [g.strip() for g in gcr]
        lcr = [g for g in gcr if g in main_rid]
        lcr = "; ".join(lcr)
        return lcr

    df[LCR_NORM] = df.apply(extract, axis=1)
    save_main_csv_zip(df=df, root_directory=root_directory)

    return df[LCR_NORM].notna().sum()
