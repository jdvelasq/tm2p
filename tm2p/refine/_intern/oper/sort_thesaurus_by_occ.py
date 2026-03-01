import pandas as pd

from tm2p._intern import Params
from tm2p._intern.data_access import load_main_csv_zip
from tm2p.enums import ThesaurusField

CHANGED = ThesaurusField.CHANGED.value
KEY = ThesaurusField.OLD.value
OCC = ThesaurusField.OCC.value
PREFERRED = ThesaurusField.PREFERRED.value
VARIANT = ThesaurusField.VARIANT.value


def sort_thesaurus_by_occ(
    params: Params,
    thesaurus_df: pd.DataFrame,
) -> pd.DataFrame:

    data_df = load_main_csv_zip(
        root_directory=params.root_directory,
        usecols=[params.source_field.value],
    )

    variant_to_preferred = _build_variant_to_preferred_mapping(thesaurus_df)

    preferred_to_occ = _build_preferred_to_occ_mapping(
        data_df=data_df,
        variant_to_preferred=variant_to_preferred,
        source_field=params.source_field.value,
    )

    thesaurus_df = _sort_by_occ(thesaurus_df, preferred_to_occ)

    return thesaurus_df


# def _build_raw_series(params, data_df):
#     raw_series = data_df[params.source_field.value].copy()
#     raw_series = raw_series.dropna()
#     raw_series = raw_series.str.split("; ").explode()
#     raw_series = raw_series.str.strip()
#     return raw_series


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
    # dataframe = dataframe.drop(columns=[OCC])

    return dataframe
