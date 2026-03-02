import pandas as pd

from tm2p._intern import Params
from tm2p.enum import ThesaurusField

from ._post_process import _post_process
from ._pre_process import _pre_process

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
SIGNATURE = ThesaurusField.SIGNATURE.value
VARIANT = ThesaurusField.VARIANT.value


def apply_exact_match_rule(
    thesaurus_df: pd.DataFrame,
    params: Params,
) -> pd.DataFrame:

    thesaurus_df = _pre_process(params=params, thesaurus_df=thesaurus_df)
    #
    thesaurus_df[PREFERRED] = thesaurus_df[PREFERRED].str.replace(
        r"\r\n|\r", "", regex=True
    )
    thesaurus_df[PREFERRED] = thesaurus_df[PREFERRED].str.strip()
    #
    thesaurus_df = _post_process(thesaurus_df=thesaurus_df)

    return thesaurus_df
