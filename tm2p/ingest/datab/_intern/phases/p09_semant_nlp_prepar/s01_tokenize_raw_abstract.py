from tm2p import Field
from tm2p.ingest.datab._intern.oper import tokenize_column


def s01_tokenize_raw_abstract(root_directory: str) -> int:

    return tokenize_column(
        source=Field.ABSTR_RAW,
        target=Field.ABSTR_TOK,
        root_directory=root_directory,
    )
