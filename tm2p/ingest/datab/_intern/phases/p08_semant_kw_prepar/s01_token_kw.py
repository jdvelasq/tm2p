from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip

from ...oper import copy_column
from .helpers import (
    add_padding,
    fix_parenthesis_spacing,
    invert_acronym_definition,
    normalize_empty_strings,
    normalize_quotes,
    remove_accents,
    remove_empty_terms,
    remove_html_tags,
    remove_leading_articles,
    remove_padding,
    remove_possessives_ampersands_and_punctuation,
    strip_surrounding_chars,
    transform_keywords_to_lower_case,
    translate,
)


def s01_token_keywordtoken_keyword(root_directory: str) -> int:

    copy_column(
        source=Field.IDXKW_RAW,
        target=Field.IDXKW_TOK,
        root_directory=root_directory,
    )

    copy_column(
        source=Field.AUTHKW_RAW,
        target=Field.AUTHKW_TOK,
        root_directory=root_directory,
    )

    df = load_main_csv_zip(root_directory)
    df = normalize_empty_strings(df)
    df = add_padding(df)
    df = remove_accents(df)
    df = transform_keywords_to_lower_case(df)
    df = remove_html_tags(df)
    df = fix_parenthesis_spacing(df)
    df = invert_acronym_definition(df)
    df = translate(df)
    df = remove_leading_articles(df)
    df = normalize_quotes(df)
    df = strip_surrounding_chars(df)
    df = remove_possessives_ampersands_and_punctuation(df)
    df = remove_empty_terms(df)
    df = remove_padding(df)

    save_main_csv_zip(df, root_directory)

    return max(
        int(df[Field.AUTHKW_TOK.value].notna().sum()),
        int(df[Field.IDXKW_TOK.value].notna().sum()),
    )
