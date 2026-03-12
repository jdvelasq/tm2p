import pandas as pd  # type: ignore

from tm2p import Field


def normalize_quotes(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.replace("ʿ", "'", regex=False)
        dataframe[col] = dataframe[col].str.replace('"', "'", regex=False)

    return dataframe
