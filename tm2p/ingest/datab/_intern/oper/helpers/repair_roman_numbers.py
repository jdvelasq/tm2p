import re

import pandas as pd  # type: ignore

ROMAN_NUMBERS = [
    "i",
    "ii",
    "iii",
    "iv",
    "v",
    "vi",
    "vii",
    "viii",
    "ix",
    "x",
]

_COMPILED_PATTERNS: list[re.Pattern] = []


def _get_compiled_patterns() -> list[re.Pattern]:
    if not _COMPILED_PATTERNS:
        _COMPILED_PATTERNS.extend(
            re.compile(r"(\( " + number + r" )\)", re.IGNORECASE)
            for number in ROMAN_NUMBERS
        )
        _COMPILED_PATTERNS.extend(
            re.compile(r"(\( and " + number + r" )\)", re.IGNORECASE)
            for number in ROMAN_NUMBERS
        )
    return _COMPILED_PATTERNS


def repair_roman_numbers(text):
    if pd.isna(text):
        return text
    text = str(text)
    for pattern in _get_compiled_patterns():
        text = pattern.sub(lambda z: z.group().lower(), text)

    return text
