from tm2p import Field

from ..oper import copy_column


def normalize_idx_key_raw(root_directory: str) -> int:

    return copy_column(
        source=Field.IDXKW_TOK,
        target=Field.IDXKW_NORM,
        root_directory=root_directory,
    )
