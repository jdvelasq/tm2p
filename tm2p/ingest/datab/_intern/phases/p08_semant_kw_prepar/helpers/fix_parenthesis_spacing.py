import pandas as pd  # type: ignore

from tm2p import Field


def fix_parenthesis_spacing(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:

        dataframe[col] = dataframe[col].str.replace(
            r"([A-Za-z0-9])([\(\[\{])",
            r"\1 \2",
            regex=True,
        )
        dataframe[col] = dataframe[col].str.replace(
            r"([A-Za-z0-9])([\)\]\}])",
            r"\1 \2",
            regex=True,
        )

        dataframe[col] = dataframe[col].str.replace(
            r"([\)\]\}])([A-Za-z0-9])",
            r"\1 \2",
            regex=True,
        )
        dataframe[col] = dataframe[col].str.replace(
            r"([\(\[\{])([A-Za-z0-9])",
            r"\1 \2",
            regex=True,
        )

    return dataframe
