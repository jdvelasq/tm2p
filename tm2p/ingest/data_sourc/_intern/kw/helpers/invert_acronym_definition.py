from typing import Optional

import pandas as pd  # type: ignore

from tm2p import Field


def invert_acronym_definition_in_list(keywords: Optional[str]) -> Optional[str]:

    if not isinstance(keywords, str):
        return keywords

    keyword_list: list[str] = keywords.split("; ")

    new_keywords = []
    for keyword in keyword_list:

        keyword = keyword.strip()

        if " (" in keyword and keyword.endswith(")") and not keyword.startswith("("):

            acronym, definition = keyword.split("(", 1)

            definition = definition[:-1]
            definition = definition.strip()
            acronym = acronym.strip()

            if len(definition.split()) > 1:  # definition has more than one word
                new_keyword = f"{definition} ( {acronym} )"
                new_keywords.append(new_keyword)
            else:
                new_keywords.append(keyword)

        else:

            new_keywords.append(keyword)

    return " ; ".join(new_keywords)


def invert_acronym_definition(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe = dataframe.copy()

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].apply(invert_acronym_definition_in_list)

    return dataframe
