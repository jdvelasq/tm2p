import pandas as pd

from tm2p.enum import ThesaurusField

CHANGED = ThesaurusField.CHANGED.value
KEY = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
VARIANT = ThesaurusField.VARIANT.value


def explode_and_merge(
    thesaurus_df: pd.DataFrame,
) -> pd.DataFrame:

    thesaurus_df = thesaurus_df.copy()
    #
    thesaurus_df[VARIANT] = thesaurus_df[VARIANT].str.split("; ")
    thesaurus_df = thesaurus_df.groupby(PREFERRED).agg(
        {
            VARIANT: lambda lists: sorted(
                dict.fromkeys(item for sublist in lists for item in sublist)
            ),
            CHANGED: "any",
        }
    )
    thesaurus_df[VARIANT] = thesaurus_df[VARIANT].str.join("; ")

    thesaurus_df = thesaurus_df.sort_values(
        by=[CHANGED, PREFERRED, VARIANT], ascending=[False, True, True]
    ).reset_index()

    thesaurus_df = thesaurus_df[[CHANGED, PREFERRED, VARIANT]].reset_index(drop=True)

    return thesaurus_df
