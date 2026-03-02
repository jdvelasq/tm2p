from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import merge_columns


def compose_key_norm(root_directory: str) -> int:

    return merge_columns(
        sources=(
            Field.AUTHKW_NORM,
            Field.IDXKW_NORM,
        ),
        target=Field.KW_NORM,
        root_directory=root_directory,
    )
