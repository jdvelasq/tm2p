from pathlib import Path
from pprint import pprint

import pandas as pd  # type: ignore


def view_dataframe():

    for folder in ["openalex", "pubmed", "scopus", "wos"]:

        print(f"Processing {folder} ...")

        filepath = Path("tests") / folder / "ingest" / "process" / "main.csv.zip"
        df = pd.read_csv(
            filepath, encoding="utf-8", low_memory=False, compression="zip"
        )

        # df.pop("ABSTR_RAW")
        # if "GCR_WOS_FORMAT" in df.columns:
        #     df.pop("GCR_WOS_FORMAT")
        txt_filepath = Path(folder + ".txt")
        df = df.head(50)
        with open(txt_filepath, "w", encoding="utf-8") as txt_file:
            txt_file.write(df.to_string(index=False))


view_dataframe()


def view_column():

    # columns = []
    field = "AUTH_RAW"

    for folder in ["openalex", "pubmed", "scopus", "wos"]:

        filepath = Path("tests") / folder / "ingest" / "process" / "main.csv.zip"
        df = pd.read_csv(
            filepath, encoding="utf-8", low_memory=False, compression="zip"
        )

        if field in df.columns:
            rows = df[field].dropna().head(10)
            print(f".... {folder} ....")
            print(rows.head())
            print()

    # series = pd.concat(columns)
    # series = series.dropna()
    # series = series.str.split("; ")
    # series = series.explode()
    # counts = series.value_counts()

    # pprint(counts)

    # df.pop("ABSTR_RAW")
    # if "GCR_WOS_FORMAT" in df.columns:
    #     df.pop("GCR_WOS_FORMAT")
    # txt_filepath = Path(folder + ".txt")
    # df = df.head(50)
    # with open(txt_filepath, "w", encoding="utf-8") as txt_file:
    #     txt_file.write(df.to_string())


# view_column()
