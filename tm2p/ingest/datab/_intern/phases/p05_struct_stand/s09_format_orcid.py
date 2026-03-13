from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p.enum import Field


def s09_format_orcid(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)

    if Field.ORCID.value in df.columns:
        df[Field.ORCID.value] = df[Field.ORCID.value].str.replace(
            "https://orcid.org/", "", regex=False
        )
        df = df.replace("ORCID: ", "ORCID:", regex=False)

        df[Field.ORCID.value] = df[Field.ORCID.value].map(
            lambda x: x[:-1] if x[-1] == ";" else x, na_action="ignore"
        )

        save_main_csv_zip(df, root_directory)

        return 1

    return 0
