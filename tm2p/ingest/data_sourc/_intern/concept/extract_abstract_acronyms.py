import re
import sys
from pathlib import Path

import pandas as pd  # type: ignore
from pandarallel import pandarallel  # type: ignore

from tm2p._intern import stdout_to_stderr
from tm2p.enum.field import Field

ACRONYMS_PATTERN = re.compile(r"\((.*?)\)")


def _extract_acronyms_from_text(text: str) -> str:
    if pd.isna(text):
        return ""
    matches = ACRONYMS_PATTERN.findall(text)
    return "; ".join(matches)


def extract_abstract_acronyms(root_directory: str) -> int:

    database_file = Path(root_directory) / "ingest" / "processed" / "main.csv.zip"

    if not database_file.exists():
        raise AssertionError(f"{database_file.name} not found")

    dataframe = pd.read_csv(
        database_file,
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    if "abstract_tokenized" not in dataframe.columns:
        return 0

    with stdout_to_stderr():
        progress_bar = True
        pandarallel.initialize(progress_bar=progress_bar, verbose=0)
        dataframe[Field.ABSTR_ACRONYM.value] = dataframe[Field.ABSTR_TOK.value].parallel_apply(_extract_acronyms_from_text)  # type: ignore[call-arg]
        sys.stderr.write("\n")

    dataframe.to_csv(
        database_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )

    return len(dataframe[Field.ABSTR_ACRONYM.value].dropna())
