from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import transform_column


def normalize_doctype_raw(root_directory: str) -> int:

    return transform_column(
        source=Field.PUBTYPE_RAW,
        target=Field.PUBTYPE_NORM,
        function=lambda x: x.str.capitalize(),
        root_directory=root_directory,
    )
