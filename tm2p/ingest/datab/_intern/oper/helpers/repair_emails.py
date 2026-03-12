import re

import pandas as pd  # type: ignore

EMAIL_PATTERN = re.compile(
    r"[a-za-z0-9. %+-]+@[a-za-z0-9.-]+\.[a-za-z]{2,}", re.IGNORECASE
)


def repair_emails(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = EMAIL_PATTERN.sub(lambda m: m.group().lower(), text)
    return text
