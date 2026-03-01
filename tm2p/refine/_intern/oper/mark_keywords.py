import pandas as pd

from tm2p import CorpusField
from tm2p._intern import Params
from tm2p._intern.data_access import load_main_csv_zip
from tm2p.enums import ThesaurusField

CHANGED = ThesaurusField.CHANGED.value
IS_KEYWORD = ThesaurusField.IS_KEYWORD.value
OCC = ThesaurusField.OCC.value
OLD = ThesaurusField.OLD.value
PREFERRED = ThesaurusField.PREFERRED.value
VARIANT = ThesaurusField.VARIANT.value


def mark_keywords(
    params: Params,
    thesaurus_df: pd.DataFrame,
) -> pd.DataFrame:

    data_df = load_main_csv_zip(
        root_directory=params.root_directory,
        # usecols=[params.source_field.value],
    )

    keywords = _extract_keywords_from_data(data_df)

    thesaurus_df = thesaurus_df.copy()
    thesaurus_df[IS_KEYWORD] = thesaurus_df[PREFERRED].apply(lambda x: x in keywords)

    return thesaurus_df


def _extract_keywords_from_data(data_df):

    keywords = set()
    for col in [
        CorpusField.AUTHKW_RAW.value,
        CorpusField.IDXKW_RAW.value,
    ]:
        series = data_df[col].dropna().str.split("; ").explode().str.strip()
        keywords.update(series.drop_duplicates().to_list())

    return keywords


def _build_raw_series(params, data_df):
    raw_series = data_df[params.source_field.value].copy()
    raw_series = raw_series.dropna()
    raw_series = raw_series.str.split("; ").explode()
    raw_series = raw_series.str.strip()
    return raw_series


def _build_variant_to_preferred_mapping(dataframe):

    dataframe = dataframe.copy()
    dataframe = dataframe[[PREFERRED, VARIANT]].copy()
    dataframe[VARIANT] = dataframe[VARIANT].str.split("; ")
    dataframe = dataframe.explode(VARIANT)
    dataframe[VARIANT] = dataframe[VARIANT].str.strip()

    variant_to_preferred = dict(zip(dataframe[VARIANT], dataframe[PREFERRED]))

    return variant_to_preferred


def _build_preferred_to_occ_mapping(data_df, variant_to_preferred, source_field):

    data_df = data_df.copy()
    data_df = data_df.dropna()

    data_df[source_field] = data_df[source_field].str.split("; ")
    data_df[source_field] = data_df[source_field].apply(
        lambda x: [variant_to_preferred.get(y.strip(), y.strip()) for y in x]
    )
    data_df[source_field] = data_df[source_field].apply(set)
    data_df = data_df.explode(source_field)

    series = data_df[source_field].value_counts()

    occ_mapping = dict(
        zip(
            series.index,
            series.to_list(),
        )
    )

    return occ_mapping


def _sort_by_occ(dataframe, occ_mapping):

    dataframe = dataframe.copy()
    dataframe[OCC] = dataframe[PREFERRED].apply(lambda x: occ_mapping.get(x, 0))
    dataframe = dataframe.sort_values([OCC, PREFERRED], ascending=[False, True])
    dataframe = dataframe.drop(columns=[OCC])

    return dataframe
