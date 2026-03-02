from pathlib import Path

import pandas as pd
from fuzzywuzzy import fuzz  # type: ignore
from tqdm import tqdm  # type: ignore

from tm2p._intern import Params
from tm2p.enum import ThesaurusField

from ._pre_process import _pre_process

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
SIGNATURE = ThesaurusField.SIGNATURE.value
VARIANT = ThesaurusField.VARIANT.value


def apply_fuzzy_cutoff_0_word_rule(
    thesaurus_df: pd.DataFrame,
    params: Params,
) -> int:

    thesaurus_df = _pre_process(params=params, thesaurus_df=thesaurus_df)
    thesaurus_df = _prepare_thesaurus(thesaurus_df=thesaurus_df)

    candidates_df = thesaurus_df[thesaurus_df["word_count"] == 1].copy()
    candidates_df = candidates_df.reset_index(drop=True)

    mapping = _compute_matches(
        thesaurus_df=candidates_df,
        similarity_cutoff=params.similarity_cutoff,
        fuzzy_threshold=0.0,
        use_word_level=False,
        word_count_tolerance=0,
    )

    _report_mergings(
        params=params,
        mapping=mapping,
        filename="candidate_mergings.txt",
    )

    return len(mapping)


def _prepare_thesaurus(thesaurus_df: pd.DataFrame) -> pd.DataFrame:

    thesaurus_df = thesaurus_df.copy()

    thesaurus_df = thesaurus_df[~thesaurus_df[PREFERRED].str.startswith("#")]

    thesaurus_df["char_length"] = thesaurus_df[PREFERRED].str.len()
    thesaurus_df["word_count"] = thesaurus_df[PREFERRED].str.split().str.len()
    thesaurus_df = thesaurus_df.sort_values(
        by=["word_count", "char_length", OCC, PREFERRED],
        ascending=[True, True, False, True],
    )
    thesaurus_df = thesaurus_df.reset_index(drop=True)

    return thesaurus_df


def _compute_matches(
    thesaurus_df: pd.DataFrame,
    similarity_cutoff: float,
    fuzzy_threshold: float,
    use_word_level: bool,
    word_count_tolerance: int,
) -> dict[str, list[str]]:

    thesaurus_df = thesaurus_df.copy()
    thesaurus_df["matched"] = False

    keys = thesaurus_df[PREFERRED].tolist()
    mergings: dict[str, list[str]] = {}

    for index, key in tqdm(
        enumerate(keys),
        total=len(keys),
        desc="  Progress",
        ncols=80,
    ):
        if thesaurus_df.loc[index, "matched"]:
            continue

        candidates = thesaurus_df[
            (thesaurus_df.index > index) & (~thesaurus_df["matched"])
        ].copy()

        if candidates.empty:
            continue

        key_word_count = len(key.split())
        candidates = candidates[
            candidates["word_count"].between(
                key_word_count - word_count_tolerance,
                key_word_count + word_count_tolerance,
            )
        ]

        if candidates.empty:
            continue

        candidates = _char_length_preselect(key, candidates, similarity_cutoff)

        if candidates.empty:
            continue

        candidates = _apply_cutoff(key, candidates, similarity_cutoff)

        if candidates.empty:
            continue

        if use_word_level:
            candidates = _apply_word_level_match(key, candidates, fuzzy_threshold)

        if candidates.empty:
            continue

        thesaurus_df.loc[candidates.index, "matched"] = True
        mergings[key] = candidates[PREFERRED].tolist()

    return mergings


def _char_length_preselect(
    key: str,
    candidates: pd.DataFrame,
    similarity_cutoff: float,
) -> pd.DataFrame:

    key_len = len(key)
    diff = int((1 - similarity_cutoff / 100.0) * key_len) + 1
    min_len = max(key_len - diff, 1)
    max_len = key_len + diff
    return candidates[
        (candidates["char_length"] >= min_len) & (candidates["char_length"] <= max_len)
    ]


def _apply_cutoff(
    key: str,
    candidates: pd.DataFrame,
    similarity_cutoff: float,
) -> pd.DataFrame:

    candidates = candidates.copy()
    candidates["cutoff_score"] = candidates[PREFERRED].apply(
        lambda x: fuzz.ratio(key, x)
    )
    return candidates[candidates["cutoff_score"] >= similarity_cutoff]


def _apply_word_level_match(
    key: str,
    candidates: pd.DataFrame,
    fuzzy_threshold: float,
) -> pd.DataFrame:

    def _score(string1: str, string2: str) -> float:
        words1 = string1.split()
        words2 = string2.split()
        shorter, longer = (
            (words1, words2) if len(words1) <= len(words2) else (words2, words1)
        )
        remaining = list(longer)
        scores = []
        for base_word in shorter:
            best_score, best_idx = 0, -1
            for i, candidate_word in enumerate(remaining):
                s = fuzz.ratio(base_word, candidate_word)
                if s > best_score:
                    best_score, best_idx = s, i
            scores.append(best_score)
            if best_idx >= 0:
                remaining.pop(best_idx)
        return sum(scores) / len(scores) if scores else 0.0

    candidates = candidates.copy()
    candidates["word_score"] = candidates[PREFERRED].apply(lambda x: _score(key, x))
    return candidates[candidates["word_score"] >= fuzzy_threshold]


def _report_mergings(
    params: Params,
    mapping: dict[str, list[str]],
    filename: str,
) -> None:

    filepath = Path(params.root_directory) / "refine" / "thesaurus" / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        for preferred, variants in mapping.items():
            f.write(f"{preferred}\n")
            for variant in variants:
                f.write(f"    {variant}\n")
