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
    df[Field.AUTHID_RAW.value] = df.apply(_repair, axis=1)
    save_main_csv_zip(df, root_directory)

    # for _, row in df.iterrows():
    #     if len(row[Field.AUTH_NORM.value].split("; ")) != len(
    #         row[Field.AUTHID_RAW.value].split("; ")
    #     ):
    #         raise ValueError(
    #             f"Mismatch in number of authors and author IDs for row {_}"
    #         )

    return int(df[Field.AUTHID_RAW.value].notna().sum())


def _repair(row):

    authid = row[Field.AUTHID_RAW.value]
    if pd.isna(authid):
        return _repair_na_row(row)
    return _repair_sequ(row)


def _repair_na_row(row):
    auth = row[Field.AUTH_FULL_NAME.value]
    auth = auth.split("; ")
    authid = [au.strip() + sequ_gener() for au in auth]
    authid = "; ".join(authid)

    return authid


def _repair_sequ(row):

    auth = row[Field.AUTH_FULL_NAME.value]
    auth = auth.split("; ")
    auth = [au.strip() for au in auth]

    authid = row[Field.AUTHID_RAW.value]
    authid = authid.lower()
    authid = authid.split("; ")

    result = []
    for au in auth:
        au_short = au.split(" ")[0].lower()
        found = False
        for x in authid:
            if au_short in x:
                result.append(x.title())
                found = True
                continue
        if found is False:
            result.append(au + sequ_gener())

    if len(result) != len(auth):
        raise ValueError(f"Could not match all authors to their IDs for row {row.name}")

    authid = "; ".join(result)

    return authid
