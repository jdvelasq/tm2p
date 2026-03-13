from tm2p import Field
from tm2p.ingest.datab._intern.oper import uppercase_keyterms


def s06_uppercase_abstract_phrases(root_directory: str) -> int:

    return uppercase_keyterms(
        source=Field.ABSTR_TOK,
        target=Field.ABSTR_UPPER,
        root_directory=root_directory,
    )
