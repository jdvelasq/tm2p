from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import merge_columns


def merge_title_and_abstract_phrases(root_directory: str) -> int:

    return merge_columns(
        sources=(
            Field.NP_ABSTR_RAW,
            Field.NP_TITLE_RAW,
        ),
        target=Field.NP_RAW,
        root_directory=root_directory,
    )
