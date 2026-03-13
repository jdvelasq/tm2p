from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field
from tm2p.ingest.datab._intern.oper.coalesc_col import coalesce_column
from tm2p.ingest.datab._intern.oper.copy_col import copy_column
from tm2p.ingest.datab._intern.oper.ltwa_col import ltwa_column


def s08_format_src_iso4(root_directory: str) -> int:

    _create_iso4_raw_column(root_directory)

    copy_column(
        source=Field.SRC_ISO4_RAW,
        target=Field.SRC_ISO4_NORM,
        root_directory=root_directory,
    )

    coalesce_column(
        source=Field.SRC_NORM,
        target=Field.SRC_ISO4_NORM,
        root_directory=root_directory,
    )

    _format_iso4_norm_column(root_directory)

    ltwa_column(
        source=Field.SRC_ISO4_NORM,
        target=Field.SRC_ISO4_NORM,
        root_directory=root_directory,
    )

    return 1


def _create_iso4_raw_column(root_directory: str) -> None:
    df = load_main_csv_zip(root_directory)
    if Field.SRC_ISO4_RAW.value not in df.columns:
        df[Field.SRC_ISO4_RAW.value] = df[Field.SRC_NORM.value].copy()
        save_main_csv_zip(df, root_directory)


def _format_iso4_norm_column(root_directory: str) -> None:

    df = load_main_csv_zip(root_directory)
    df[Field.SRC_ISO4_NORM.value] = (
        df[Field.SRC_ISO4_NORM.value]
        .str.upper()
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(":", "", regex=False)
    )
    save_main_csv_zip(df, root_directory)
