from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import count_column_items


def calculate_numref_global(root_directory: str) -> int:

    return count_column_items(
        source=Field.GCR_RAW,
        target=Field.N_GCR,
        root_directory=root_directory,
    )


#
