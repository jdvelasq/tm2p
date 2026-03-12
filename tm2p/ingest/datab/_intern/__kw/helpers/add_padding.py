import pandas as pd  # type: ignore

from tm2p import Field


def add_padding(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].apply(lambda x: f" {x} " if pd.notna(x) else x)

    return dataframe
