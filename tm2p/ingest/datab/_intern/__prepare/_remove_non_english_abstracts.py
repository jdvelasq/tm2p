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


def _process_file(csv_file: Path, field_name: str) -> int:

    df = pd.read_csv(csv_file, encoding="utf-8", low_memory=False)
    n_before = len(df)
    df["abs_lang"] = df[field_name].apply(_detect_language)
    df = df[df["abs_lang"] == "en"]
    df = df.drop(columns=["abs_lang"])
    n_after = len(df)
    n_removed = n_before - n_after

    if n_removed > 0:
        df.to_csv(csv_file, encoding="utf-8", index=False)

    return n_removed


def _remove_from_database(path: Path, field_name: str) -> int:

    if not path.exists():
        return 0

    total_removed = 0

    csv_files = list(path.glob("*.csv"))

    for csv_file in csv_files:
        removed = _process_file(csv_file, field_name)
        total_removed += removed

    return total_removed


def remove_non_english_abstracts(root_directory: str) -> int:
    """:meta private:"""

    openalex_path = Path(root_directory) / "ingest" / "raw" / "openalex"
    scopus_path = Path(root_directory) / "ingest" / "raw" / "scopus" / "main"
    wos_path = Path(root_directory) / "ingest" / "raw" / "wos"

    removed = 0
    removed += _remove_from_database(openalex_path, "abstract")
    removed += _remove_from_database(scopus_path, "Abstract")
    removed += _remove_from_database(wos_path, "abstract")

    return removed
