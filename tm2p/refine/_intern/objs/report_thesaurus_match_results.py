import pandas as pd

from tm2p._intern import Params
from tm2p.enum import ThesaurusField

from .thesaurus_match_result import ThesaurusMatchResult

FLAG = ThesaurusField.CHANGED.value
KEY = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
VARIANT = ThesaurusField.VARIANT.value


def report_thesaurus_match_results(
    params: Params,
    df: pd.DataFrame,
) -> ThesaurusMatchResult:

    df = df.copy()

    counting = df[ThesaurusField.PREFERRED.value].value_counts()
    counting = counting[counting > 1]
    duplicated_items = counting.index.to_list()
    df = df[df[ThesaurusField.PREFERRED.value].isin(duplicated_items)]

    num_candidates = self.compute_num_candidates(df)
    num_groups = self.compute_num_groups(df)
    df = self.add_occ_info(df)
    reporting_df = self.generate_reporting_dataframe(df)
    candidates_filepath = self.get_candidates_filepath()
    self.generate_candidates_txt_file(
        filepath=candidates_filepath, dataframe=reporting_df
    )

    return ThesaurusMatchResult(
        colored_output=params.colored_output,
        output_file=str(candidates_filepath),
        thesaurus_file=params.thesaurus_file,
        msg=f"Found {num_candidates} match candidates for merging.",
        success=True,
        field=params.source_field.value,
        num_candidates=num_candidates,
        num_groups=num_groups,
    )
