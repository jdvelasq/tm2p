from tm2p import Field
from tm2p.ingest.datab._intern.oper import uppercase_keyterms


def uppercase_title_phrases(root_directory: str) -> int:

    return uppercase_keyterms(
        source=Field.TITLE_TOK,
        target=Field.TITLE_UPPER,
        root_directory=root_directory,
    )
