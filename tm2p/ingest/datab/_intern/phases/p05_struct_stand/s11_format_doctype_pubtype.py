from tm2p._intern.data_access import load_main_csv_zip
from tm2p.enum import Field
from tm2p.ingest.datab._intern.oper import transform_column


def s11_format_doctype_pubtype(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    if Field.DOCTYPE.value in df.columns:
        transform_column(
            source=Field.DOCTYPE,
            target=Field.DOCTYPE,
            function=lambda x: x.str.capitalize(),
            root_directory=root_directory,
        )

    if Field.PUBTYPE.value in df.columns:
        transform_column(
            source=Field.PUBTYPE,
            target=Field.PUBTYPE,
            function=lambda x: x.str.capitalize(),
            root_directory=root_directory,
        )

    return 1
