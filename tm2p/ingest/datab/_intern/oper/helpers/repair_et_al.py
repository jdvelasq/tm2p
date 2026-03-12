import re

import pandas as pd  # type: ignore

ET_AL_PATTERN = re.compile(r"\b[A-Z][A-Z_]+_ET_AL\b")


def repair_et_al(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = ET_AL_PATTERN.sub(lambda m: m.group().replace("_", " ").lower(), text)
    return text
