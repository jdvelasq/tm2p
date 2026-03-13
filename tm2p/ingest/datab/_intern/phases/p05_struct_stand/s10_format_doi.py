from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s10_format_doi(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df[Field.DOI.value] = df[Field.DOI.value].str.replace(
        "https://doi.org/", "", regex=False
    )
    save_main_csv_zip(df, root_directory)

    return 1
