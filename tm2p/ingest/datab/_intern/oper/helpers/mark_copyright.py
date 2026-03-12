import re

import pandas as pd  # type: ignore

from tm2p._intern.packag_data.word_lists import load_builtin_word_list

_COMPILED_PATTERNS: list[re.Pattern] = []


def _get_compiled_patterns() -> list[re.Pattern]:
    if not _COMPILED_PATTERNS:
        # copyright_regex = load_text_processing_terms("copyright_regex.txt")
        copyright_regex = load_builtin_word_list("copyright.txt")
        _COMPILED_PATTERNS.extend(
            re.compile(r"(" + regex + r")") for regex in copyright_regex
        )
    return _COMPILED_PATTERNS


def mark_copyright(text) -> str:
    if pd.isna(text):
        return text
    text = str(text)
    for pattern in _get_compiled_patterns():
        text = pattern.sub(lambda m: m.group().replace(" ", "_"), text)
    return text
