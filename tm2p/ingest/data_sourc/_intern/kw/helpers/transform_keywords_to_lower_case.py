import pandas as pd  # type: ignore

from tm2p import Field


def transform_keywords_to_lower_case(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.lower()

    return dataframe
