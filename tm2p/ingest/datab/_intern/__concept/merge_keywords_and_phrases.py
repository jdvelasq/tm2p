from tm2p import Field
from tm2p.ingest.datab._intern.oper import copy_column, merge_columns


def merge_keywords_and_phrases(root_directory: str) -> int:

    result = merge_columns(
        sources=(
            Field.KW_TOK,
            Field.NP_RAW,
        ),
        target=Field.CONCEPT_RAW,
        root_directory=root_directory,
    )

    copy_column(
        source=Field.CONCEPT_RAW,
        target=Field.CONCEPT_NORM,
        root_directory=root_directory,
    )

    return result
