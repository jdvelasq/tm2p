from tm2p import Field
from tm2p.ingest.datab._intern.oper import extract_uppercase


def s08_extract_abstract_phrases(root_directory: str) -> int:

    return extract_uppercase(
        source=Field.ABSTR_UPPER,
        target=Field.NP_ABSTR_RAW,
        root_directory=root_directory,
    )
