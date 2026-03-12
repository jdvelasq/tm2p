import re

import pandas as pd  # type: ignore

from tm2p._intern.packag_data.word_lists import load_builtin_word_list

_COMPILED_PATTERNS: list[tuple[str, re.Pattern]] = []


def _get_compiled_patterns() -> list[tuple[str, re.Pattern]]:
    if not _COMPILED_PATTERNS:
        patterns = load_builtin_word_list("discourse_connectors.txt")
        _COMPILED_PATTERNS.extend(
            (phrase, re.compile(r"\b(" + re.escape(phrase) + r")\b"))
            for phrase in patterns
        )
    return _COMPILED_PATTERNS


def mark_discursive_patterns(text):
    if pd.isna(text):
        return text
    text = str(text)
    for phrase, pattern in _get_compiled_patterns():
        if phrase in text:
            text = pattern.sub(lambda m: m.group().lower().replace(" ", "_"), text)
    return text
