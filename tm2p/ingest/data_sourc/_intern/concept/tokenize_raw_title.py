from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import tokenize_column


def tokenize_raw_title(root_directory: str) -> int:

    return tokenize_column(
        source=Field.TITLE_RAW,
        target=Field.TITLE_TOK,
        root_directory=root_directory,
    )
