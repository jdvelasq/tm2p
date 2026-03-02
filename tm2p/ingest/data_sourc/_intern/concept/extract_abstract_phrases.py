from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import extract_uppercase


def extract_abstract_phrases(root_directory: str) -> int:

    return extract_uppercase(
        source=Field.ABSTR_UPPER,
        target=Field.NP_ABSTR_RAW,
        root_directory=root_directory,
    )
