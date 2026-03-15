import string
import sys
from typing import Optional

import pandas as pd  # type: ignore
import spacy
from pandarallel import pandarallel  # type: ignore

from tm2p import Field
from tm2p._intern import stdout_to_stderr
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip

spacy_nlp = spacy.load("en_core_web_lg")


def s04_extract_spacy_phrases(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory=root_directory)

    with stdout_to_stderr():
        progress_bar = True
        pandarallel.initialize(progress_bar=progress_bar, verbose=0)
        df[Field.NP_SPACY.value] = df.parallel_apply(  # type: ignore
            _process_row,
            axis=1,
        )
        sys.stderr.write("\n")

    save_main_csv_zip(df=df, root_directory=root_directory)

    phrases = df[Field.NP_SPACY.value].dropna()
    phrases = phrases.str.split("; ").explode()
    phrases = phrases.drop_duplicates()
    n_phrases = len(phrases)

    return n_phrases


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
    phrases_str = "; ".join(sorted(phrases))

    return phrases_str
