import string
import sys
from pathlib import Path
from typing import Optional

import pandas as pd  # type: ignore
import spacy
from pandarallel import pandarallel  # type: ignore

from tm2p import Field
from tm2p._intern import stdout_to_stderr

spacy_nlp = spacy.load("en_core_web_lg")


def _process_row(row: pd.Series) -> Optional[str]:

    phrases: list[str] = []

    if not pd.isna(row[Field.ABSTR_TOK.value]):
        phrases.extend(
            chunk.text for chunk in spacy_nlp(row[Field.ABSTR_TOK.value]).noun_chunks
        )

    if not pd.isna(row[Field.TITLE_TOK.value]):
        phrases.extend(
            chunk.text for chunk in spacy_nlp(row[Field.TITLE_TOK.value]).noun_chunks
        )

    if not phrases:
        return None

    punctuation = set(string.punctuation.replace("_", ""))
    phrases = [
        term for term in phrases if not any(char in term for char in punctuation)
    ]

    vowels = set("aeiou")
    phrases = [term for term in phrases if any(char in vowels for char in term)]

    phrases = list(dict.fromkeys(phrases))
    phrases_str = "; ".join(phrases)

    return phrases_str


def extract_spacy_phrases(root_directory: str) -> int:

    database_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"

    if not database_file.exists():
        raise AssertionError(f"{database_file.name} not found")

    dataframe = pd.read_csv(
        database_file,
        encoding="utf-8",
        compression="zip",
        low_memory=False,
    )

    with stdout_to_stderr():
        progress_bar = True
        pandarallel.initialize(progress_bar=progress_bar, verbose=0)
        dataframe[Field.NP_SPACY.value] = dataframe.parallel_apply(  # type: ignore
            _process_row,
            axis=1,
        )
        sys.stderr.write("\n")

    dataframe.to_csv(
        database_file,
        sep=",",
        encoding="utf-8",
        index=False,
        compression="zip",
    )

    phrases = dataframe[Field.NP_SPACY.value].dropna()
    phrases = phrases.str.split("; ").explode()
    phrases = phrases.drop_duplicates()
    n_phrases = len(phrases)

    return n_phrases
