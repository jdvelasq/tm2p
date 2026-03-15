import re

from textblob import Word  # type: ignore

from tm2p import Field
from tm2p._intern.packag_data import load_builtin_word_list
from tm2p.ingest.datab._intern.oper import copy_column, merge_columns
from tm2p.ingest.datab._intern.oper.transform_col import transform_column

STOPWORDS = load_builtin_word_list("stopwords.txt")


def s02_create_words(root_directory: str) -> int:

    transform_column(
        source=Field.CONCEPT_RAW,
        target=Field.WORD_RAW,
        function=_transform,
        root_directory=root_directory,
    )

    copy_column(
        source=Field.WORD_RAW,
        target=Field.WORD_NORM,
        root_directory=root_directory,
    )

    return merge_columns(
        sources=(
            Field.CONCEPT_RAW,
            Field.WORD_RAW,
        ),
        target=Field.DESCRIPTOR_RAW,
        root_directory=root_directory,
    )


def _transform(series):

    series = _split_in_words(series)
    series = _remove_stopwords(series)
    series = _remove_invalid_words(series)
    series = _singularize(series)
    series = _sort_words(series)

    return series.str.join("; ")


def _sort_words(series):
    series = series.map(
        sorted,
        na_action="ignore",
    )

    return series


def _singularize(series):
    series = series.map(
        lambda x: (
            set(Word(word).singularize().lemmatize() for word in x)
            if isinstance(x, set)
            else x
        ),
        na_action="ignore",
    )

    return series


def _remove_invalid_words(series):
    def _remove(words):
        if not isinstance(words, set):
            return words
        return set(word for word in words if re.match(r"^[\w\s-]+$", word))

    return series.map(_remove, na_action="ignore")


def _remove_stopwords(series):
    series = series.map(
        lambda x: x - STOPWORDS if isinstance(x, set) else x, na_action="ignore"
    )
    return series


def _split_in_words(series):
    series = series.str.replace(";", "", regex=False)
    series = series.str.split()
    series = series.map(lambda x: [y.strip() for y in x], na_action="ignore")
    series = series.map(set, na_action="ignore")
    return series
