import re

import pandas as pd  # type: ignore

from tm2p import Field


def remove_leading_articles(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:

        for article in ["and", "an", "a", "the"]:

            dataframe[col] = dataframe[col].apply(
                lambda x, art=article: (
                    [re.sub(f"^ {art} ", " ", z) for z in x]
                    if isinstance(x, list)
                    else x
                )
            )

            dataframe[col] = dataframe[col].apply(
                lambda x, art=article: (
                    [re.sub(f"; {art} ", "; ", z) for z in x]
                    if isinstance(x, list)
                    else x
                )
            )

    return dataframe
