import re

import pandas as pd  # type: ignore

ISSN_PATTERN = re.compile(r"\b issn \b", re.IGNORECASE)
ISBN_PATTERN = re.compile(r"\b isbn \b", re.IGNORECASE)
EISSN_PATTERN = re.compile(r"\b eissn \b", re.IGNORECASE)


def repair_isbn_issn(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = ISSN_PATTERN.sub(" issn ", text)
    text = ISBN_PATTERN.sub(" isbn ", text)
    text = EISSN_PATTERN.sub(" eissn ", text)
    return text
