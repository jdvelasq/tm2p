from pathlib import Path

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip


def create_concept_thesaurus(root_directory: str) -> int:

    dataframe = load_main_csv_zip(
        root_directory=root_directory, usecols=[Field.CONCEPT_RAW.value]
    )
    dataframe = dataframe.dropna()
    dataframe = dataframe.rename(columns={Field.CONCEPT_RAW.value: "item"})
    series = dataframe["item"]
    series = series.str.split("; ")
    series = series.explode()
    series = series.str.strip()
    counting = series.value_counts()
    counting_df = counting.to_frame(name="count")
    counting_df = counting_df.reset_index()
    counting_df = counting_df.sort_values(by=["item", "count"], ascending=[True, True])

    filepath = Path(root_directory) / "refine" / "thesaurus" / "concepts.the.txt"

    with open(filepath, "w", encoding="utf-8") as file:
        for _, row in counting_df.iterrows():
            term = row["item"]
            file.write(f"{term}\n")
            file.write(f"    {term}\n")

    return len(counting_df)
