from tm2p import Field

from ..oper import copy_column


def normalize_auth_key_raw(root_directory: str) -> int:

    return copy_column(
        source=Field.AUTHKW_TOK,
        target=Field.AUTHKW_NORM,
        root_directory=root_directory,
    )
