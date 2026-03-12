import re

import ahocorasick  # type: ignore
import pandas as pd  # type: ignore

from tm2p._intern.packag_data.word_lists import load_builtin_word_list


def _initialize_scaffolding_automaton():
    automaton = ahocorasick.Automaton()
    for phrase in load_builtin_word_list("rhetorical_scaffolding.txt"):
        automaton.add_word(phrase.lower(), phrase)
    automaton.make_automaton()
    return automaton


AHOCORASICK = _initialize_scaffolding_automaton()

_COMPILED_PATTERNS: dict[str, re.Pattern] = {}


def _extract_scaffolding(text):
    text_lower = text.lower()
    seen_positions = {}
    for end_idx, phrase in AHOCORASICK.iter(text_lower):
        start_idx = end_idx - len(phrase) + 1
        if start_idx not in seen_positions or len(phrase) > len(
            seen_positions[start_idx][0]
        ):
            seen_positions[start_idx] = (phrase, end_idx)
    result = []
    last_end = -1
    for start in sorted(seen_positions):
        phrase, end_idx = seen_positions[start]
        if start >= last_end:
            result.append(phrase)
            last_end = end_idx + 1
    return result


def mark_scaffolding(text):

    if pd.isna(text):
        return text
    text = str(text)

    scaffolding_phrases = _extract_scaffolding(text)

    for phrase in scaffolding_phrases:
        if phrase not in _COMPILED_PATTERNS:
            _COMPILED_PATTERNS[phrase] = re.compile(
                r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE
            )
        pattern = _COMPILED_PATTERNS[phrase]
        text = pattern.sub(lambda m: m.group().lower().replace(" ", "_"), text)

    return text
