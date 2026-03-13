from typing import Optional

import pandas as pd  # type: ignore
from langdetect import LangDetectException, detect  # type: ignore

from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def _detect_language(text: Optional[str]) -> Optional[str]:

    if pd.isna(text):
        return None

    try:
        return detect(str(text))
    except LangDetectException:
        return None


def remov_non_english_abstr(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    abstr_col = None
    if "abstract" in df.columns.to_list():
        abstr_col = "abstract"
    elif "AB" in df.columns.to_list():
        abstr_col = "AB"
    elif "Abstract" in df.columns.to_list():
        abstr_col = "Abstract"
    else:
        return 0

    df["abs_lang"] = df[abstr_col].apply(_detect_language)
    df = df[df["abs_lang"] == "en"]

    n_before = len(df)
    df = df.drop(columns=["abs_lang"])
    n_after = len(df)
    n_removed = n_before - n_after

    if n_removed > 0:
        save_main_csv_zip(df, root_directory)

    return n_removed
