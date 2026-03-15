from pathlib import Path

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip

SIZE = 30


def s04_generate_review_table(root_directory: str) -> None:

    df = load_main_csv_zip(root_directory=root_directory).head(100)

    for col in df.columns:
        if df[col].dtype == "object":
            max_size = df[col].str.len().max()
            if Field.REC_ID.value == col:
                df[col] = df[col].str[:50]
            elif max_size > SIZE:
                df[col] = df[col].str[:SIZE]

    filename = Path(root_directory) / "refine" / "review_table.txt"
    df = df.head(50)

    with open(filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(df.to_markdown(index=False))
