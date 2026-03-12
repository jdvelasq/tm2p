import re
from typing import Optional

import pandas as pd  # type: ignore

_COMPILED_PATTERNS: list[re.Pattern] = []


def _get_compiled_patterns() -> list[re.Pattern]:
    if not _COMPILED_PATTERNS:
        _COMPILED_PATTERNS.append(re.compile(r"\b([a-z_\(\)\d])+\b"))
        _COMPILED_PATTERNS.append(re.compile(r"\b\._([a-z_\(\)\d])+_:\b"))
    return _COMPILED_PATTERNS


def repair_lowercase_text(text: Optional[str]) -> Optional[str]:
    if pd.isna(text):
        return None
    text = str(text)
    for pattern in _get_compiled_patterns():
        text = pattern.sub(lambda m: m.group().replace("_", " "), text)
    return text
