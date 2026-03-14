import pandas as pd  # type: ignore

from tm2p import Field

KEYWORDS_MAX_LENGTH = 60


def fix_keyword_separators(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].apply(
            lambda x: (
                x.replace(",", ";")
                if isinstance(x, str) and ";" not in x and len(x) > KEYWORDS_MAX_LENGTH
                else x
            )
        )

    return dataframe
