from tm2p import Field
from tm2p.ingest.datab._intern.oper import transform_column


def normalize_doctype_raw(root_directory: str) -> int:

    return transform_column(
        source=Field.DOCTYPE_RAW,
        target=Field.DOCTYPE_NORM,
        function=lambda x: x.str.capitalize(),
        root_directory=root_directory,
    )
