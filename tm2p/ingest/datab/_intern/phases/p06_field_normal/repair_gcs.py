from tm2p.enum import Field

from ...oper.transform_col import transform_column


def repair_gcs(root_directory: str) -> int:

    return transform_column(
        source=Field.GCS,
        target=Field.GCS,
        function=lambda w: w.fillna(0).astype(int),
        root_directory=root_directory,
    )
