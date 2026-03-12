import pandas as pd  # type: ignore

from tm2p import Field

LEFT_CHARS = ("(", "[", "{", "'", '"')
RIGHT_CHARS = (")", "]", "}", "'", '"')


def _remove_chars(text: str) -> str:

    if text.startswith(tuple(LEFT_CHARS)) and text.endswith(tuple(RIGHT_CHARS)):
        return text[1:-1].strip()

    return text


def strip_surrounding_chars(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.split(";")
        dataframe[col] = dataframe[col].apply(
            lambda x: ([item.strip() for item in x] if isinstance(x, list) else x),
        )
        dataframe[col] = dataframe[col].apply(
            lambda x: ([item.strip() for item in x] if isinstance(x, list) else x),
        )
        dataframe[col] = dataframe[col].apply(
            lambda x: (
                [_remove_chars(item) for item in x] if isinstance(x, list) else x
            ),
        )
        dataframe[col] = dataframe[col].apply(
            lambda x: (
                [item for item in x if not item.isdigit()] if isinstance(x, list) else x
            ),
        )
        dataframe[col] = dataframe[col].apply(
            lambda x: (
                [item for item in x if item != ""] if isinstance(x, list) else x
            ),
        )
        dataframe[col] = dataframe[col].apply(
            lambda x: ([item.strip() for item in x] if isinstance(x, list) else x),
        )
        dataframe[col] = dataframe[col].str.join("; ")
        dataframe[col] = dataframe[col].apply(
            lambda x: f" {x} " if isinstance(x, str) else x
        )

    return dataframe
