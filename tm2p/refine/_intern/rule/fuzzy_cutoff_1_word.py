import pandas as pd

from tm2p._intern import Params
from tm2p.enum import ThesaurusField

from ._pre_process import _pre_process
from .fuzzy_cutoff_0_word import _compute_matches, _prepare_thesaurus, _report_mergings

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
SIGNATURE = ThesaurusField.SIGNATURE.value
VARIANT = ThesaurusField.VARIANT.value


def apply_fuzzy_cutoff_1_word_rule(
    thesaurus_df: pd.DataFrame,
    params: Params,
) -> pd.DataFrame:

    thesaurus_df = _pre_process(params=params, thesaurus_df=thesaurus_df)
    thesaurus_df = _prepare_thesaurus(thesaurus_df=thesaurus_df)

    candidates_df = thesaurus_df[thesaurus_df["word_count"] >= 2].copy()
    candidates_df = candidates_df.reset_index(drop=True)

    mapping = _compute_matches(
        thesaurus_df=candidates_df,
        similarity_cutoff=params.similarity_cutoff,
        fuzzy_threshold=params.fuzzy_threshold,
        use_word_level=True,
        word_count_tolerance=1,
    )

    _report_mergings(
        params=params,
        mapping=mapping,
        filename="candidate_mergings.txt",
    )

    return thesaurus_df
