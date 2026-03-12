import re

import pandas as pd  # type: ignore

_APOSTROPHE_LOWERCASE_PATTERN = re.compile(r"([a-z]) ' S_([A-Z])")
_APOSTROPHE_UPPERCASE_PATTERN = re.compile(r"([A-Z]) ' S_([A-Z])")


def repair_apostrophes(text) -> str:
    if pd.isna(text):
        return text
    text = str(text)
    text = _APOSTROPHE_LOWERCASE_PATTERN.sub(r"\1 ' s \2", text)
    text = _APOSTROPHE_UPPERCASE_PATTERN.sub(r"\1_\2", text)
    return text
