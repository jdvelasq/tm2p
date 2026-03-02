import pandas as pd  # type: ignore

from tm2p import Field


def normalize_empty_strings(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].map(
            lambda x: pd.NA if isinstance(x, str) and x.strip() == "" else x
        )

    return dataframe
