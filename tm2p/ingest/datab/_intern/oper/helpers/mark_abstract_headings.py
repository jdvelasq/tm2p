import re
from typing import Optional

import pandas as pd  # type: ignore

COMPOUND_STRUCTURED_ABSTRACT_HEADINGS = [
    "actionable insights",
    "aim and background",
    "aim and methods",
    "aims / objectives",
    "application design",
    "applications of this study",
    "authors ' conclusions",
    "background / objectives",
    "background and aims",
    "background and objective",
    "background and purpose",
    "case description",
    "clinical impact",
    "clinical registration",
    "clinical relevance",
    "clinical significance",
    "clinical trial registration",
    "conclusion , significance and impact study",
    "conclusion and relevance",
    "contribution of the paper",
    "data collection and analysis",
    "data sources",
    "data visualization tools",
    "design / methodology / approach",
    "design / methods",
    "design / settings",
    "design methodology approach",
    "discussion and conclusions",
    "discussion and evaluation",
    "diverse perspectives",
    "ethical considerations",
    "ethics and dissemination",
    "findings and originality",
    "findings and value added",
    "graphical abstract",
    "impact and implications",
    "impact statement",
    "implications for practice and policy",
    "implications for practice",
    "implications for theory and practice",
    "improvements / applications",
    "intended outcomes",
    "interests design / methodology / approach",
    "key findings",
    "key messages",
    "key results",
    "limitations and implications",
    "main findings",
    "main measures",
    "main outcome ( s )",
    "main outcome measure",
    "main outcome measures",
    "main outcomes and measures",
    "main results",
    "managerial implications",
    "material / methods",
    "material and methods",
    "materials and methods",
    "methodological quality assessment tools include",
    "methodology / results",
    "methodology and results",
    "methods , procedures , process",
    "methods / statistical analysis",
    "methods and analysis",
    "methods and findings",
    "methods and results",
    "novel / additive information",
    "novelty / originality of this study",
    "novelty / originality",
    "objectives / scope",
    "originality / value",
    "originality and value",
    "our contributions include",
    "outcome measures",
    "paper aims",
    "patient or public contribution",
    "place and duration of study",
    "practical examples",
    "practical implications",
    "practical relevance",
    "practice implications",
    "problem definition",
    "public interest summary",
    "purpose of review",
    "purpose of the article",
    "purpose of the study",
    "recent findings",
    "reporting quality assessment tool",
    "research background",
    "research design",
    "research limitations / implications",
    "research method",
    "research question",
    "results , observations , conclusions",
    "results and discussion",
    "results show",
    "review methods",
    "scholarly critique",
    "scientific discussion",
    "search methods",
    "selection criteria",
    "setting / participants / intervention",
    "settings and participants",
    "social implications",
    "some key results",
    "study design",
    "subjects and methods",
    "subjects and methods",
    "teaching implications",
    "the topics include",
    "theoretical framework",
]


_PATTERN_CACHE: dict[str, list[re.Pattern]] = {}


def _build_heading_pattern(prefix: str, heading: str) -> re.Pattern:
    escaped_heading = re.escape(heading)
    if prefix == r"^":
        return re.compile(f"^({escaped_heading})( :)", re.IGNORECASE)
    return re.compile(f"({prefix})({escaped_heading})( :)", re.IGNORECASE)


def _get_patterns_for_prefix(prefix: str) -> list[re.Pattern]:
    if prefix not in _PATTERN_CACHE:
        _PATTERN_CACHE[prefix] = [
            _build_heading_pattern(prefix, heading)
            for heading in COMPOUND_STRUCTURED_ABSTRACT_HEADINGS
        ]
    return _PATTERN_CACHE[prefix]


def _normalize_heading_match(match: re.Match) -> str:
    groups = match.groups()
    if len(groups) == 2:
        heading, suffix = groups
        return heading.lower().replace(" ", "_") + suffix
    prefix, heading, suffix = groups
    return prefix + heading.lower().replace(" ", "_") + suffix


def mark_abstract_headings(text: Optional[str]) -> Optional[str]:
    if pd.isna(text):
        return None

    text = str(text)

    for prefix in (r"^", r"\. ", r"\? ", r"\) "):
        for pattern in _get_patterns_for_prefix(prefix):
            text = pattern.sub(_normalize_heading_match, text)

    return text
