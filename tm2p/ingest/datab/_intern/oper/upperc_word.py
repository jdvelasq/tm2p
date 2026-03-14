import re
import sys
from functools import lru_cache

import pandas as pd  # type: ignore
from pandarallel import pandarallel  # type: ignore

from tm2p import Field
from tm2p._intern import stdout_to_stderr
from tm2p._intern.packag_data.word_lists import load_builtin_word_list

from ._file_dispatch import get_file_operations
from .helpers import (
    extract_urls,
    mark_abstract_headings,
    mark_copyright,
    mark_discursive_patterns,
    mark_scaffolding,
    repair_abstract_headings,
    repair_apostrophes,
    repair_emails,
    repair_et_al,
    repair_lowercase_text,
    repair_measurement_units,
    repair_roman_numbers,
    repair_strange_cases,
    repair_urls,
)

STOPWORDS: set[str] = set(
    phrase.strip().lower()
    for phrase in load_builtin_word_list("stopwords.txt")
    if phrase.strip()
)


# ----------------------------------------------------------------------------
@lru_cache(maxsize=1024)
def _compile_pattern(pattern: str) -> re.Pattern:
    return re.compile(r"\b" + re.escape(pattern) + r"\b")


# ----------------------------------------------------------------------------
def _highlight_words(text):

    if pd.isna(text):
        return text

    text = str(text)
    for word in text.split():

        if re.match(r"^[a-z][a-z0-9]*$", word):
            pattern = _compile_pattern(word)
            text = pattern.sub(word.upper(), text)

    return text


# ----------------------------------------------------------------------------
def _normalize(text):

    if pd.isna(text):
        return None

    url_matches = extract_urls(text)
    text = mark_copyright(text)
    text = mark_abstract_headings(text)
    text = mark_discursive_patterns(text)
    text = mark_scaffolding(text)
    #
    text = _highlight_words(text)
    #
    text = repair_apostrophes(text)
    text = repair_measurement_units(text)
    text = repair_urls(text, url_matches)
    text = repair_lowercase_text(text)
    text = repair_abstract_headings(text)
    text = repair_et_al(text)
    text = mark_scaffolding(text)
    text = repair_roman_numbers(text)
    text = repair_emails(text)
    text = repair_strange_cases(text)

    return text


# ----------------------------------------------------------------------------


def uppercase_words(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: str = "ignore",
) -> int:

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    with stdout_to_stderr():
        progress_bar = True
        pandarallel.initialize(progress_bar=progress_bar, verbose=0)
        dataframe[target.value] = dataframe[source.value].parallel_apply(_normalize)
        sys.stderr.write("\n")

    save_data(df=dataframe, root_directory=root_directory)

    return int(dataframe[target.value].notna().sum())
