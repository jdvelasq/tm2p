from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s02_repair_scopus_authid(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df[Field.AUTHID_NORM.value] = df.apply(_repair, axis=1)
    save_main_csv_zip(df, root_directory)

    return int(df[Field.AUTHID_NORM.value].notna().sum())


def _repair(row):

    authid = row[Field.AUTHID_RAW.value]
    if authid[-1] == ";":
        authid = authid[:-1]
    return authid
