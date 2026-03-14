import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.datab._intern.oper import transform_column


def s04_extr_openalex_ctry(root_directory: str) -> int:

    _repair_ctry_iso2(root_directory=root_directory)

    return _create_ctry_col(root_directory=root_directory)


def _repair_ctry_iso2(root_directory: str) -> None:

    def _repair(row):
        ctry_iso2 = row[Field.CTRY_ISO2.value]
        if pd.isna(ctry_iso2):
            if pd.isna(row[Field.AUTH_FULL_NAME.value]):
                return "[UNKNOWN]"
            n_auth = row[Field.AUTH_FULL_NAME.value].count("; ") + 1
            return "; ".join(["[UNKNOWN]"] * n_auth)
        ctry_iso2 = ctry_iso2.split("; ")
        ctry_iso2 = [crty.strip() for crty in ctry_iso2]
        ctry_iso2 = [ctry if ctry != "" else "[UNKNOWN]" for ctry in ctry_iso2]
        if all(ctry == "[UNKNOWN]" for ctry in ctry_iso2):
            return "[UNKNOWN]"
        return "; ".join(ctry_iso2)

    df = load_main_csv_zip(root_directory=root_directory)
    df[Field.CTRY_ISO2.value] = df.apply(_repair, axis=1)
    save_main_csv_zip(df=df, root_directory=root_directory)


def _create_ctry_col(root_directory: str) -> int:

    ctry_to_alpha2 = load_builtin_mapping("country_to_alpha2.the.json")
    alpha2_to_ctry = {v: k for k, v in ctry_to_alpha2.items()}

    def _extract(series: pd.Series) -> pd.Series:
        series = series.str.split("; ")
        series = series.map(
            lambda x: [alpha2_to_ctry.get(i, "[UNKNOWN]") for i in x],
            na_action="ignore",
        )
        series = series.str.join("; ")
        return series

    return transform_column(
        source=Field.CTRY_ISO2,
        target=Field.CTRY,
        function=_extract,
        root_directory=root_directory,
    )
