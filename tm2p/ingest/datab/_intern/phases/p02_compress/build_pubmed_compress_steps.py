# CODE_REVIEW: 2026-01-26

import zipfile
from pathlib import Path

from tm2p._intern import Params

from ...step import Step


def build_pubmed_compress_steps(params: Params) -> list[Step]:

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Compressing PubMed raw data",
            function=_compress_files,
            kwargs=common_kwargs,
        ),
    ]


def _compress_files(root_directory: str) -> None:

    filepath = Path(root_directory) / "ingest" / "raw"
    txt_files = list(filepath.glob("*.txt"))

    for txt_file in txt_files:
        zip_file = txt_file.with_suffix(".txt.zip")
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(txt_file, arcname=txt_file.name)
        txt_file.unlink()
