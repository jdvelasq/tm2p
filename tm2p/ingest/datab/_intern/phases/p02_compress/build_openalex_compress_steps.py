# CODE_REVIEW: 2026-01-26

from pathlib import Path

import pandas as pd  # type: ignore

from tm2p._intern import Params

from ...step import Step


def build_openalex_compress_steps(params: Params) -> list[Step]:

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Compressing OpenAlex raw data",
            function=_compress_files,
            kwargs=common_kwargs,
        ),
    ]


def _compress_files(root_directory: str) -> None:

    filepath = Path(root_directory) / "ingest" / "raw"
    csv_files = list(filepath.glob("*.csv"))

    for csv_file in csv_files:
        zip_file = str(csv_file) + ".zip"
        df = pd.read_csv(csv_file, encoding="utf-8", low_memory=False)
        df.to_csv(zip_file, index=False, encoding="utf-8", compression="zip")
        csv_file.unlink()
