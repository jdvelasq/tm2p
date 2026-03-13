from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip
from tm2p._intern.packag_data import load_builtin_word_list
from tm2p.ingest.datab._intern.oper import transform_column

from ._intern.country_replacements import _COUNTRY_REPLACEMENTS


def s04_extr_scopus_ctry(root_directory: str) -> int:

    _create_ctry_col(root_directory=root_directory)
    _create_ctry_thesaurus(root_directory=root_directory)

    return 1


def _create_ctry_col(root_directory: str) -> int:

    def _extract(series: pd.Series) -> pd.Series:

        for pat, repl in _COUNTRY_REPLACEMENTS:
            series = series.replace(pat, repl)

        ctry = series.str.split("; ")
        ctry = ctry.apply(lambda x: [c.split(",")[-1] for c in x])

        ctry = ctry.apply(
            lambda x: ["[n/a]" if y not in country_names else y for y in x]
        )

        ctry = ctry.str.join("; ").str.strip().str.replace(".", "", regex=False)
        return ctry

    country_names = load_builtin_word_list("country_names.txt")

    return transform_column(
        source=Field.AFFIL_RAW,
        target=Field.CTRY,
        function=_extract,
        root_directory=root_directory,
    )


def _create_ctry_thesaurus(root_directory: str) -> int:

    def _zip(row):
        affil = row[Field.AFFIL_RAW].str.split("; ")
        ctry = row[Field.CTRY].str.split("; ")

        if pd.isna(affil) or pd.isna(ctry):
            return pd.NA

        return list(zip(ctry, affil))

    df = load_main_csv_zip(root_directory=root_directory)

    ctry_affil = df.apply(_zip, axis=1)
    ctry_affil = (
        ctry_affil.dropna()
        .explode()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    thdf = pd.DataFrame(
        {
            "ctry": ctry_affil.apply(lambda x: x[0]),
            "affil": ctry_affil.apply(lambda x: x[1]),
        }
    )
    grouped = thdf.groupby("ctry", as_index=False).apply(list)

    filepath = Path(root_directory) / "refine" / "thesaurus" / "ctry.the.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        for _, row in grouped.iterrows():
            ctry = row["ctry"]
            f.write(f"{ctry}\n")
            for affil in sorted(row["affil"]):
                f.write(f"    {affil}\n")

    return 0
