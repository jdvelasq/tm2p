import re
from typing import Optional

import pandas as pd  # type: ignore

from .mark_abstract_headings import COMPOUND_STRUCTURED_ABSTRACT_HEADINGS

SINGLE_STRUCTURED_ABSTRACT_HEADINGS = [
    "abbreviations",
    "abstract",
    "aim",
    "aims",
    "analysis",
    "applications",
    "approach",
    "background",
    "conclusion",
    "conclusions",
    "context",
    "contribution",
    "design",
    "discussion",
    "evaluation",
    "evidence",
    "features",
    "findings",
    "funding",
    "goal",
    "highlights",
    "impact",
    "implementation",
    "implications",
    "interpretation",
    "intervention",
    "interventions",
    "introduction",
    "keywords",
    "limitations",
    "method",
    "methodology",
    "methods",
    "objective",
    "objectives",
    "originality",
    "outcomes",
    "overview",
    "participants",
    "patients",
    "place",
    "program",
    "purpose",
    "recommendations",
    "result",
    "results",
    "setting",
    "settings",
    "significance",
    "subjects",
    "suggestions",
    "summary",
    "uniqueness",
    "value",
]

_COMPILED_PATTERNS: list[tuple[str, re.Pattern]] = []


def _get_compiled_patterns() -> list[tuple[str, re.Pattern]]:
    if not _COMPILED_PATTERNS:
        _COMPILED_PATTERNS.extend(
            (phrase, re.compile(r"\b(" + re.escape(phrase) + r")\b"))
            for phrase in COMPOUND_STRUCTURED_ABSTRACT_HEADINGS
        )
    return _COMPILED_PATTERNS


def repair_abstract_headings(text: Optional[str]) -> Optional[str]:
    if pd.isna(text):
        return None
    text = str(text)
    for term in (
        COMPOUND_STRUCTURED_ABSTRACT_HEADINGS + SINGLE_STRUCTURED_ABSTRACT_HEADINGS
    ):

        # Corrects structured abstract markers at the beginning of the paragraph:
        regex = re.compile(r"^" + term.replace(" ", "_") + " :", re.IGNORECASE)
        text = re.sub(regex, term.lower() + " :", text)

        # Corrects structured abstract markers inside the paragraph:
        regex = re.compile(r"\. " + term.replace(" ", "_") + " :", re.IGNORECASE)
        text = re.sub(regex, ". " + term.lower() + " :", text)

        regex = re.compile(r"\) " + term.replace(" ", "_") + " :", re.IGNORECASE)
        text = re.sub(regex, ") " + term.lower() + " :", text)

        regex = re.compile(r"\? " + term.replace(" ", "_") + " :", re.IGNORECASE)
        text = re.sub(regex, "? " + term.lower() + " :", text)

        regex = re.compile(r"' " + term.replace(" ", "_") + " :", re.IGNORECASE)
        text = re.sub(regex, "' " + term.lower() + " :", text)

        ## ending with [

        regex = re.compile(r"^" + term.replace(" ", "_") + r" \[", re.IGNORECASE)
        text = re.sub(regex, term.lower() + " :", text)

        regex = re.compile(r"\. " + term.replace(" ", "_") + r" \[", re.IGNORECASE)
        text = re.sub(regex, ". " + term.lower() + " [", text)

        regex = re.compile(r"\) " + term.replace(" ", "_") + r" \[", re.IGNORECASE)
        text = re.sub(regex, ") " + term.lower() + " [", text)

        regex = re.compile(r"\? " + term.replace(" ", "_") + r" \[", re.IGNORECASE)
        text = re.sub(regex, "? " + term.lower() + " [", text)

        regex = re.compile(r"' " + term.replace(" ", "_") + r" \[", re.IGNORECASE)
        text = re.sub(regex, "' " + term.lower() + " [", text)

    return text
