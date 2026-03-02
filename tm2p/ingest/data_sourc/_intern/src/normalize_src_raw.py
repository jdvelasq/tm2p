from pathlib import Path

from tm2p import Field
from tm2p.ingest.data_sourc._intern.oper import transform_column

from ..oper.data_file import DataFile


def _normalize(text):
    text = text.str.replace("<.*?>", "", regex=True)
    return text


def normalize_srctitle_raw(root_directory: str) -> int:

    ref_file = Path(root_directory) / "ingest" / "processed" / "references.csv.zip"

    if ref_file.exists():

        transform_column(
            source=Field.SRC_RAW,
            target=Field.SRC_NORM,
            function=_normalize,
            root_directory=root_directory,
            file=DataFile.REFERENCES,
        )

    return transform_column(
        source=Field.SRC_RAW,
        target=Field.SRC_NORM,
        function=_normalize,
        root_directory=root_directory,
        file=DataFile.MAIN,
    )
