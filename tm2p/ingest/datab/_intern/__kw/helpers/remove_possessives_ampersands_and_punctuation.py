import pandas as pd  # type: ignore

from tm2p import Field


def remove_possessives_ampersands_and_punctuation(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.replace("'s ", " ", regex=False)
        dataframe[col] = dataframe[col].str.replace("'", "", regex=False)
        dataframe[col] = dataframe[col].str.replace('"', "", regex=False)
        dataframe[col] = dataframe[col].str.replace("&", " and ", regex=False)
        dataframe[col] = dataframe[col].str.replace(".", "", regex=False)
        dataframe[col] = dataframe[col].str.replace(",", "", regex=False)
        dataframe[col] = dataframe[col].str.replace(":", "", regex=False)
        dataframe[col] = dataframe[col].str.replace(" - ", "", regex=False)
        dataframe[col] = dataframe[col].str.replace("\u2013", "-", regex=False)

    return dataframe
