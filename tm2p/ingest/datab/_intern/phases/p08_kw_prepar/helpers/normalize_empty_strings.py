import pandas as pd  # type: ignore

from tm2p import Field


def normalize_empty_strings(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        df[col] = df[col].map(
            lambda x: pd.NA if isinstance(x, str) and x.strip() == "" else x
        )

    return df
