from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip

from ...oper import merge_columns


def s04_compose_kw_tok(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    if Field.IDXKW_RAW.value not in df.columns:
        return 0
    if Field.AUTHKW_RAW.value not in df.columns:
        return 0

    return merge_columns(
        sources=(
            Field.AUTHKW_TOK,
            Field.IDXKW_TOK,
        ),
        target=Field.KW_TOK,
        root_directory=root_directory,
    )
