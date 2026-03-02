import pandas as pd

from tm2p._intern import Params
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.enum import ThesaurusField

from ._post_process import _post_process
from ._pre_process import _pre_process

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
SIGNATURE = ThesaurusField.SIGNATURE.value
VARIANT = ThesaurusField.VARIANT.value


def _add_padding(series):
    return series.str.replace(r"\s+", " ", regex=True).apply(lambda x: f" {x} ")


def _remove_padding(series):
    return series.str.replace(r"\s+", " ", regex=True).str.strip()


def _replace_space_separated_words_with_hyphen(series):
    valid_hyphenated_words = load_builtin_word_list("valid_hyphenated_words.txt")
    for valid_word in valid_hyphenated_words:
        pattern = f" {valid_word.replace('-', ' ')} "
        series = series.str.replace(pattern, f" {valid_word} ", regex=False)
    return series


def _replace_concatenated_words_with_hyphen(series):
    valid_hyphenated_words = load_builtin_word_list("valid_hyphenated_words.txt")
    for valid_word in valid_hyphenated_words:
        pattern = f" {valid_word.replace('-', '')} "
        series = series.str.replace(pattern, f" {valid_word} ", regex=False)
    return series


def _replace_space_separated_invalid_hyphenated_words(series):
    invalid_hyphenated_words = load_builtin_word_list("invalid_hyphenated_words.txt")
    for word in invalid_hyphenated_words:
        valid_word = word.replace("-", "")
        pattern = f" {word.replace('-', ' ')} "
        series = series.str.replace(pattern, f" {valid_word} ", regex=False)
    return series


def apply_hyphenation_rule(
    thesaurus_df: pd.DataFrame,
    params: Params,
) -> pd.DataFrame:

    thesaurus_df = _pre_process(params=params, thesaurus_df=thesaurus_df)
    #
    thesaurus_df[PREFERRED] = _add_padding(thesaurus_df[PREFERRED])
    #
    thesaurus_df[PREFERRED] = _replace_space_separated_words_with_hyphen(
        thesaurus_df[PREFERRED]
    )
    thesaurus_df[PREFERRED] = _replace_concatenated_words_with_hyphen(
        thesaurus_df[PREFERRED]
    )

    thesaurus_df[PREFERRED] = _replace_concatenated_words_with_hyphen(
        thesaurus_df[PREFERRED]
    )
    thesaurus_df[PREFERRED] = _replace_space_separated_invalid_hyphenated_words(
        thesaurus_df[PREFERRED]
    )
    #
    thesaurus_df[PREFERRED] = _remove_padding(thesaurus_df[PREFERRED])
    #
    thesaurus_df = _post_process(thesaurus_df=thesaurus_df)

    return thesaurus_df
