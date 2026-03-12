from tm2p import Field
from tm2p.ingest.datab._intern.oper import extract_uppercase


def extract_title_phrases(root_directory: str) -> int:

    return extract_uppercase(
        source=Field.TITLE_UPPER,
        target=Field.NP_TITLE_RAW,
        root_directory=root_directory,
    )
