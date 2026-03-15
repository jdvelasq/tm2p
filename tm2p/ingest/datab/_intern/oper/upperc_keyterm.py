import re
import sys
from typing import Optional

import pandas as pd  # type: ignore
from pandarallel import pandarallel  # type: ignore

from tm2p import Field
from tm2p._intern import stdout_to_stderr
from tm2p._intern.packag_data.word_lists import load_builtin_word_list

from ._file_dispatch import get_file_operations
from .helpers import (
    extract_urls,
    join_consecutive_descriptors,
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

_COMPILED_PATTERNS: list[tuple[str, re.Pattern]] = []


# ----------------------------------------------------------------------------
def _get_project_noun_phrases(dataframe: pd.DataFrame) -> set[str]:

    noun_phrases = set()

    for column in [
        Field.NP_SPACY.value,
        Field.NP_TEXTBLOB.value,
    ]:
        if column in dataframe.columns:
            for entry in dataframe[column].dropna():
                phrases = [phrase.strip() for phrase in entry.split(";")]
                noun_phrases.update(phrases)

    return noun_phrases


# ----------------------------------------------------------------------------
def _get_builtin_noun_phrases() -> set[str]:
    noun_phrases = load_builtin_word_list("noun_phrases.txt")
    processed_noun_phrases = {
        phrase.strip().lower().replace("_", " ")
        for phrase in noun_phrases
        if phrase.strip()
    }
    return processed_noun_phrases


# ----------------------------------------------------------------------------
def _get_acronyms(dataframe: pd.DataFrame) -> set[str]:

    acronyms = set()

    if Field.ACRONYM.value in dataframe.columns:
        for entry in dataframe[Field.ACRONYM.value].dropna():
            phrases = [phrase.strip() for phrase in entry.split(";")]
            acronyms.update(phrases)

    return acronyms


# ----------------------------------------------------------------------------
def _clean_terms(terms: set[str]) -> set[str]:

    stopwords = load_builtin_word_list("stopwords.txt")
    cleaned_terms = set()
    for term in terms:
        term_lower = term.lower()
        if (
            term_lower not in stopwords
            and len(term_lower) > 1
            and "(" not in term_lower
            and "," not in term_lower
            and not any(char.isdigit() for char in term)
        ):
            cleaned_terms.add(term)
    return cleaned_terms


# ----------------------------------------------------------------------------
def _get_project_keywords(dataframe: pd.DataFrame) -> set[str]:

    keywords: set[str] = set()

    for column in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        if column in dataframe.columns:
            series = dataframe[column].dropna()
            series = series.str.replace(r"[\"'#!]", "", regex=True)
            series = series.str.replace(r"\(.*\)", "", regex=True)
            series = series.str.replace(r"\[.*\]", "", regex=True)
            series = series.str.lower()
            series = series.str.split("; ")
            series = series.explode()
            series = series.str.strip()
            series = series[series.str.len() > 2]
            series = series[~series.str.contains(r"\d", regex=True)]
            keywords.update(series)

    return keywords


# ----------------------------------------------------------------------------
def _get_compiled_patterns(dataframe: pd.DataFrame) -> list[tuple[str, re.Pattern]]:

    if not _COMPILED_PATTERNS:

        patterns = _get_project_noun_phrases(dataframe)
        patterns.update(_get_builtin_noun_phrases())
        patterns.update(_get_acronyms(dataframe))
        patterns = _clean_terms(patterns)
        patterns.update(_get_project_keywords(dataframe))

        patterns_list = sorted(
            patterns,
            key=lambda x: (len(x.split(" ")), x),
            reverse=True,
        )

        _COMPILED_PATTERNS.extend(
            (pattern, re.compile(r"\b" + re.escape(pattern) + r"\b"))
            for pattern in patterns_list
        )

        _COMPILED_PATTERNS.sort(
            key=lambda x: (len(x[0].split(" ")), x[0]), reverse=True
        )

    return _COMPILED_PATTERNS


# ----------------------------------------------------------------------------
def _highlight_patterns(text):

    if pd.isna(text):
        return text

    text = str(text)
    for phrase, pattern in _COMPILED_PATTERNS:
        if phrase in text:
            text = pattern.sub(lambda m: m.group().upper().replace(" ", "_"), text)

    return text


# ----------------------------------------------------------------------------
def _normalize(text):

    if pd.isna(text):
        return None

    try:
        url_matches = extract_urls(text)
        text = mark_copyright(text)
        text = mark_abstract_headings(text)
        text = mark_discursive_patterns(text)
        text = mark_scaffolding(text)
        #
        text = _highlight_patterns(text)
        #
        text = repair_apostrophes(text)
        text = join_consecutive_descriptors(text)
        text = repair_measurement_units(text)
        text = repair_urls(text, url_matches)
        text = repair_lowercase_text(text)
        text = repair_abstract_headings(text)
        text = repair_et_al(text)
        text = mark_scaffolding(text)
        text = repair_roman_numbers(text)
        text = repair_emails(text)
        text = repair_strange_cases(text)
    except Exception as e:
        sys.stderr.write(f"Error processing text: {e}\n")
        sys.stderr.flush()
        raise e

    return text


# ----------------------------------------------------------------------------


def uppercase_keyterms(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: Optional[str] = None,
) -> int:

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    _get_compiled_patterns(dataframe)

    with stdout_to_stderr():
        progress_bar = True
        pandarallel.initialize(progress_bar=progress_bar, verbose=0)
        dataframe[target.value] = dataframe[source.value].parallel_apply(_normalize)
        sys.stderr.write("\n")

    save_data(df=dataframe, root_directory=root_directory)

    return int(dataframe[target.value].notna().sum())
