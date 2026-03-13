from functools import lru_cache

import pandas as pd  # type: ignore

from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p._intern.packag_data import load_builtin_csv
from tm2p.enum import Field


def s13_set_scopus_asjc(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    if not (Field.ISSN.value in df.columns or Field.ISSNE.value in df.columns):
        return 0

    asjc = _load_asjc()

    issn = dict(
        zip(
            asjc[Field.ISSN.value].dropna(),
            asjc[Field.ASJC.value].dropna(),
        )
    )

    eissn = dict(
        zip(
            asjc[Field.ISSNE.value].dropna(),
            asjc[Field.ASJC.value].dropna(),
        )
    )

    df[Field.ASJC.value] = None

    if Field.ISSN.value in df.columns:
        df[Field.ASJC.value] = df[Field.ISSN.value].map(issn)

    if Field.ISSNE.value in df.columns:
        df[Field.ASJC.value] = df[Field.ASJC.value].fillna(
            df[Field.ISSNE.value].map(eissn)
        )

    non_null_count = int(df[Field.ASJC.value].notna().sum())

    save_main_csv_zip(df, root_directory)

    return non_null_count


@lru_cache(maxsize=1)
def _load_asjc() -> pd.DataFrame:
    return load_builtin_csv(filename="asjc.csv")
