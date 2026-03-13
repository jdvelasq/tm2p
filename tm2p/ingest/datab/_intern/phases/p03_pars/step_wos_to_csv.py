import zipfile
from pathlib import Path

import pandas as pd  # type: ignore


def step_wos_to_csv(root_directory: str) -> int:
    """:meta private:"""

    filepath = Path(root_directory) / "ingest" / "raw"
    zip_files = list(filepath.glob("*.zip"))

    _generate_main_csv_zip_file(root_directory, zip_files)

    return len(zip_files)


def _generate_main_csv_zip_file(root_directory, zip_files):

    dfs = []
    for zip_file in zip_files:
        df = _process_zip_file(zip_file)
        dfs.append(df)

    if not dfs:
        return

    main_path = Path(root_directory) / "ingest" / "process" / "main.csv.zip"
    concat_df = pd.concat(dfs, ignore_index=True)
    concat_df = concat_df.drop_duplicates()
    concat_df.to_csv(main_path, index=False, encoding="utf-8", compression="zip")


def _process_zip_file(zip_file: Path) -> pd.DataFrame:

    text = _read_zip_file(zip_file)
    text_records = _get_records_from_text(text)
    records_list = _record_to_mapping(text_records)

    df = pd.DataFrame(records_list)

    return df


def _read_zip_file(zip_file: Path) -> str:

    with zipfile.ZipFile(zip_file, "r", zipfile.ZIP_DEFLATED) as zf:
        lines = []
        for name in zf.namelist():
            with zf.open(name) as f:
                lines.extend(f.read().decode("utf-8").splitlines())

    lines = [
        line
        for line in lines
        if not (
            line.strip().startswith("\ufeffFN ")
            or line.strip().startswith("VR 1.0")
            or line.strip().startswith("EF")
        )
    ]
    return "\n".join(lines)


def _get_records_from_text(text: str) -> list[str]:

    records = text.split("\nER\n")
    return [record.strip() for record in records if record.strip()]


def _record_to_mapping(records: list[str]) -> list[dict[str, str]]:

    mappings = []
    for record in records:

        mapping = {}

        lines = record.split("\n")
        current_key = None
        for line in lines:

            if not line:
                continue

            if line[0] != " ":
                current_key = line[:2]
                mapping[current_key] = [line[3:].strip()]
            elif current_key is not None:
                assert (
                    current_key is not None
                ), "Continuation line found without a current key"
                mapping[current_key].append(line.strip())

        mappings.append(mapping)

    result: list[dict[str, str]] = []
    for m in mappings:
        current_mapping = {}
        for key, value in m.items():
            if key[:2] in ("AB", "TI", "OI", "DE", "ID"):
                current_mapping[key] = " ".join(value)
            else:
                current_mapping[key] = "; ".join(value)
        result.append(current_mapping)

    return result
