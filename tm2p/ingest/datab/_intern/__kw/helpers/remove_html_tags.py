import pandas as pd  # type: ignore

from tm2p import Field


def remove_html_tags(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.replace(r"<[^>]+>", "", regex=True)

    return dataframe
