from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip

from ...oper import copy_column


def s03_normal_auth_idx_key_tok(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    if Field.IDXKW_RAW.value not in df.columns:
        return 0
    if Field.AUTHKW_RAW.value not in df.columns:
        return 0

    r1 = copy_column(
        source=Field.AUTHKW_TOK,
        target=Field.AUTHKW_NORM,
        root_directory=root_directory,
    )
    r2 = copy_column(
        source=Field.IDXKW_TOK,
        target=Field.IDXKW_NORM,
        root_directory=root_directory,
    )

    return r1 + r2
