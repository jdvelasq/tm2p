import re

import pandas as pd  # type: ignore

URL_PATTERN = re.compile(r"https?://[^\s]+")


def extract_urls(text: str) -> str:
    if pd.isna(text):
        return ""
    return "; ".join(URL_PATTERN.findall(text))
