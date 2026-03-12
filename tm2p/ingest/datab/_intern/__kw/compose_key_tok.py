from tm2p import Field

from ..oper import merge_columns


def compose_key_tok(root_directory: str) -> int:

    return merge_columns(
        sources=(
            Field.AUTHKW_TOK,
            Field.IDXKW_TOK,
        ),
        target=Field.KW_TOK,
        root_directory=root_directory,
    )
