from tm2p._intern.packag_data import load_builtin_word_list

from .country_replacements import _COUNTRY_REPLACEMENTS


def extract_country_name_from_string(affiliation: str) -> str:

    country = affiliation.split(",")[-1].strip()

    for pat, repl in _COUNTRY_REPLACEMENTS:
        country = country.replace(pat, repl)

    country_names = load_builtin_word_list("country_names.txt")
    if country not in country_names:
        country = "[n/a]"

    return country
