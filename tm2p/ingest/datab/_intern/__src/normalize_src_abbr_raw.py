from pathlib import Path

from tm2p import Field
from tm2p.ingest.datab._intern.oper.coalesc_col import coalesce_column
from tm2p.ingest.datab._intern.oper.ltwa_col import ltwa_column
from tm2p.ingest.datab._intern.oper.transform_col import transform_column

from ..oper.data_file import DataFile


def _transform(x):
    x = x.str.replace(".", "", regex=False)
    x = x.str.replace(",", "", regex=False)
    x = x.str.upper()
    return x


def normalize_srctitle_abbr_raw(root_directory: str) -> int:

    ref_file = Path(root_directory) / "ingest" / "process" / "references.csv.zip"

    if ref_file.exists():
        coalesce_column(
            source=Field.SRC_NORM,
            target=Field.SRC_ISO4_NORM,
            root_directory=root_directory,
            file=DataFile.REFERENCES,
        )

        transform_column(
            source=Field.SRC_ISO4_NORM,
            target=Field.SRC_ISO4_NORM,
            function=_transform,
            root_directory=root_directory,
            file=DataFile.REFERENCES,
        )

    coalesce_column(
        source=Field.SRC_NORM,
        target=Field.SRC_ISO4_NORM,
        root_directory=root_directory,
        file=DataFile.MAIN,
    )

    transform_column(
        source=Field.SRC_ISO4_NORM,
        target=Field.SRC_ISO4_NORM,
        function=_transform,
        root_directory=root_directory,
        file=DataFile.MAIN,
    )

    return ltwa_column(
        source=Field.SRC_ISO4_NORM,
        target=Field.SRC_ISO4_NORM,
        root_directory=root_directory,
        file=DataFile.MAIN,
    )
