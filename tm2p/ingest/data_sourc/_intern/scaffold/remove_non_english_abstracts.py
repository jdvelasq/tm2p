from pathlib import Path
from typing import Optional

import pandas as pd  # type: ignore
from langdetect import LangDetectException, detect  # type: ignore


def _detect_language(text: Optional[str]) -> Optional[str]:
    if pd.isna(text):
        return None

    try:
        return detect(str(text))
    except LangDetectException:
        return None


def _process_file(csv_file: Path) -> int:

    df = pd.read_csv(csv_file, encoding="utf-8", low_memory=False)
    n_before = len(df)
    df["abs_lang"] = df["Abstract"].apply(_detect_language)
    df = df[df["abs_lang"] == "en"]
    df = df.drop(columns=["abs_lang"])
    n_after = len(df)
    n_removed = n_before - n_after

    if n_removed > 0:
        df.to_csv(csv_file, encoding="utf-8", index=False)

    return n_removed


def remove_non_english_abstracts(root_directory: str) -> int:
    """:meta private:"""

    raw_dir = Path(root_directory) / "ingest" / "raw" / "scopus" / "main"

    if not raw_dir.exists():
        return 0

    total_removed = 0

    csv_files = list(raw_dir.glob("*.csv"))

    for csv_file in csv_files:
        removed = _process_file(csv_file)
        total_removed += removed

    return total_removed
