from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip
from tm2p.ingest.datab._intern.oper import merge_columns


def s05_compose_key_norm(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    if Field.IDXKW_RAW.value not in df.columns:
        return 0
    if Field.AUTHKW_RAW.value not in df.columns:
        return 0

    return merge_columns(
        sources=(
            Field.AUTHKW_NORM,
            Field.IDXKW_NORM,
        ),
        target=Field.KW_NORM,
        root_directory=root_directory,
    )
