import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.ingest.datab._intern.oper.copy_col import copy_column

from ._intern import sequ_gener


def s02_repair_wos_authid(root_directory: str) -> int:

    copy_column(
        source=Field.ORCID,
        target=Field.AUTHID_RAW,
        root_directory=root_directory,
    )

    df = load_main_csv_zip(root_directory)
    df[Field.AUTHID_NORM.value] = df.apply(_repair, axis=1)
    save_main_csv_zip(df, root_directory)

    return int(df[Field.AUTHID_NORM.value].notna().sum())


def _repair(row):

    authid = row[Field.AUTHID_RAW.value]
    if pd.isna(authid):
        return _repair_na_row(row)
    return _repair_sequ(row)


def _repair_na_row(row):
    auth = row[Field.AUTH_NORM.value]
    auth = auth.split("; ")
    authid = [au.strip() + sequ_gener() for au in auth]
    return "; ".join(authid)


def _repair_sequ(row):

    auth = row[Field.AUTH_NORM.value]
    auth = auth.split("; ")
    auth = [au.strip() for au in auth]

    authid = row[Field.AUTHID_RAW.value]
    authid = authid.split("; ")
    authid = [au.strip() for au in authid]

    result = []
    for au, auid in zip(auth, authid):
        if pd.isna(auid):
            result.append(au.strip() + sequ_gener())
        else:
            result.append(auid.strip())

    return "; ".join(result)
