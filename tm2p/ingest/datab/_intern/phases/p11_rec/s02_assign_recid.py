import numpy as np
import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s02_assign_recid(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    wos_format = (
        _get_author(df)
        + _get_year(df)
        + ", "
        + _get_source_title(df)
        + _get_volume(df)
        + _get_page_start(df)
        + _get_doi(df)
    )

    duplicated_mask = wos_format.duplicated()
    index = wos_format.index[duplicated_mask]
    if len(index) > 0:
        wos_format.loc[index] += ", " + df[Field.TITLE_RAW.value].loc[index].str[
            :29
        ].str.upper().str.replace(".", "").str.replace(" - ", " ").str.replace(
            ",", ""
        ).str.replace(
            ":", ""
        ).str.replace(
            "-", ""
        ).str.replace(
            "'", ""
        )

    df[Field.REC_ID.value] = wos_format.copy()
    df = df.drop_duplicates(subset=[Field.REC_ID.value])

    non_null_count = int(df[Field.REC_ID.value].notna().sum())

    save_main_csv_zip(df, root_directory)

    return non_null_count


def _get_author(dataframe):
    return dataframe[Field.AUTH_FIRST.value].map(
        lambda x: (x.split(" ")[0].strip() if not pd.isna(x) else "[Anonymous]")
    )


def _get_source_title(dataframe):

    source_title = dataframe[Field.SRC_ISO4_NORM.value].copy()
    source_title_isna = source_title.map(pd.isna)
    source_title = pd.Series(
        np.where(
            source_title_isna,
            dataframe[Field.SRC_NORM.value].str[:29],
            source_title,
        )
    )

    return (
        source_title.str.upper()
        .str.replace("JOURNAL", "J")
        .str.replace(" OF ", " ")
        .str.replace(".", "")
        .str.replace(" - ", " ")
        .str.replace(",", "")
        .str.replace(":", "")
        .str.replace("-", "")
        .map(lambda x: x if not pd.isna(x) else "")
    )


def _get_year(dataframe):
    return ", " + dataframe[Field.YEAR.value].map(str).str.replace(
        ".0", "", regex=False
    )


def _get_volume(dataframe):
    if Field.VOL.value not in dataframe.columns:
        return ""
    return dataframe[Field.VOL.value].map(
        lambda x: ", V" + str(x).replace(".0", "") if not pd.isna(x) else ""
    )


def _get_page_start(dataframe):
    if Field.PG_FIRST.value not in dataframe.columns:
        return ""
    return dataframe[Field.PG_FIRST.value].map(
        lambda x: ", P" + str(x).replace(".0", "") if not pd.isna(x) else ""
    )


def _get_doi(dataframe):
    if Field.DOI.value not in dataframe.columns:
        return ""
    return dataframe[Field.DOI.value].map(str).str.replace("^nan$", "", regex=True)
