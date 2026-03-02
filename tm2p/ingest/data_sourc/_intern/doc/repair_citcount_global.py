from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import transform_column


def repair_citcount_global(root_directory: str) -> int:

    return transform_column(
        source=Field.GCS,
        target=Field.GCS,
        function=lambda w: w.fillna(0).astype(int),
        root_directory=root_directory,
    )
