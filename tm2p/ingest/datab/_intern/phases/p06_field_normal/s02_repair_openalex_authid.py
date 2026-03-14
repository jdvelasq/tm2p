import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip

from ._intern import sequ_gener


def s02_repair_openalex_authid(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df[Field.AUTHID_RAW.value] = df.apply(_repair, axis=1)
    save_main_csv_zip(df, root_directory)

    return int(df[Field.AUTHID_RAW.value].notna().sum())


def _repair(row):

    authid = row[Field.AUTHID_RAW.value]
    if pd.isna(authid):
        return _repair_na_row(row)
    return _repair_sequ(row)


def _repair_na_row(row):
    auth = row[Field.AUTH_NORM.value]
    if pd.isna(auth):
        return pd.NA
    auth = auth.split("; ")
    authid = [au.strip() + sequ_gener() for au in auth]
    return "; ".join(authid)


def _repair_sequ(row):

    auth = row[Field.AUTH_NORM.value]
    if pd.isna(auth):
        return pd.NA

    auth = auth.split("; ")
    auth = [au.strip() for au in auth]

    authid = row[Field.AUTH_NORM.value]
    authid = authid.split("; ")
    authid = [au.strip() for au in authid]

    result = []
    for au, auid in zip(auth, authid):
        if pd.isna(auid) or auid == "":
            result.append(au.strip() + sequ_gener())
        else:
            result.append(auid.strip())

    if len(result) < len(auth):
        n = len(auth) - len(result)
        result += [sequ_gener() for _ in range(n)]

    return "; ".join(result)
