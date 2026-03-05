import re
from pathlib import Path

import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import (
    get_references_csv_zip_path,
    load_main_csv_zip,
    load_references_csv_zip,
    save_main_csv_zip,
)

_SELECTED_FIELDS = [
    Field.RID.value,
    Field.TITLE_RAW.value,
    Field.AUTH_RAW.value,
    Field.YEAR.value,
]


def _clean_text(text):
    """:meta private:"""
    text = (
        text.str.lower()
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(":", "", regex=False)
        .str.replace("-", " ", regex=False)
        .str.replace("_", " ", regex=False)
        .str.replace("'", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("  ", " ", regex=False)
    )
    return text


def _prepare_cited_references(root_directory: str) -> pd.DataFrame:

    references = load_main_csv_zip(root_directory=root_directory)
    references = references[[Field.GCR_RAW.value]].copy()
    references = references.dropna()
    references = references.rename(columns={Field.GCR_RAW.value: "text"})  # type: ignore
    references["text"] = references["text"].str.split(";")
    references = references.explode("text")
    references["text"] = references["text"].str.strip()
    references = references.drop_duplicates()
    references = references.reset_index(drop=True)
    references["key"] = _clean_text(references["text"])

    return references


def _prepare_main_documents(root_directory: str) -> pd.DataFrame:

    main_df = load_main_csv_zip(root_directory=root_directory)

    main_df = main_df[_SELECTED_FIELDS]
    main_df = main_df.dropna()
    references_path = get_references_csv_zip_path(root_directory)
    if references_path.exists():
        references_df = load_references_csv_zip(root_directory=root_directory)
        references_df = references_df[_SELECTED_FIELDS].dropna()
        dataframe = pd.concat([main_df, references_df], axis=0)
        dataframe = dataframe.drop_duplicates()
    else:
        dataframe = main_df

    dataframe[Field.AUTH_FIRST.value] = (
        dataframe[Field.AUTH_RAW.value]
        .str.split(" ")
        .map(lambda x: x[0].lower().replace(",", ""))
    )
    dataframe[Field.TITLE_RAW.value] = dataframe[Field.TITLE_RAW.value].str.lower()
    dataframe[Field.TITLE_RAW.value] = _clean_text(dataframe[Field.TITLE_RAW.value])
    dataframe[Field.AUTH_RAW.value] = _clean_text(dataframe[Field.AUTH_RAW.value])
    dataframe[Field.YEAR.value] = dataframe[Field.YEAR.value].astype(str)
    dataframe = dataframe.sort_values(by=[Field.RID.value])  # type: ignore

    return dataframe


def _create_references_thesaurus_file(root_directory: str) -> None:

    dataframe = load_main_csv_zip(root_directory=root_directory)
    dataframe = dataframe[[Field.GCR_RID.value]].copy().dropna()
    dataframe[Field.GCR_RID.value] = dataframe[Field.GCR_RID.value].str.split("; ")
    dataframe = dataframe.explode(Field.GCR_RID.value)  # type: ignore
    dataframe[Field.GCR_RID.value] = dataframe[Field.GCR_RID.value].str.strip()
    dataframe["rec_id"] = dataframe[Field.GCR_RID.value].apply(
        lambda x: x.split(" @ ")[0].strip() if " @ " in x else "[n/a]"
    )
    dataframe["ref"] = dataframe[Field.GCR_RID.value].apply(
        lambda x: x.split(" @ ")[1].strip() if " @ " in x else "[n/a]"
    )

    # counting = dataframe["ref"].value_counts()
    # dataframe["ref"] = dataframe["ref"].apply(
    #     lambda x: f"{x} # occ: {counting.get(x, 0)}"
    # )

    dataframe = dataframe[["rec_id", "ref"]]
    groupby_df = dataframe.groupby("rec_id", as_index=False).agg({"ref": list})
    groupby_df["ref"] = groupby_df["ref"].apply(sorted)
    groupby_df = groupby_df.sort_values(by=["rec_id"], ascending=True)

    filepath = Path(root_directory) / "refine" / "thesaurus" / "references.the.txt"

    with open(filepath, "w", encoding="utf-8") as file:
        for _, row in groupby_df.iterrows():
            rec_id = row["rec_id"]
            if rec_id == "[n/a]":
                continue
            file.write(f"{rec_id}\n")
            for ref in row["ref"]:
                file.write(f"    {ref}\n")


def _create_mapping(
    main_documents: pd.DataFrame,
    cited_references: pd.DataFrame,
) -> dict[str, list[str]]:

    mapping = {}
    remaining_references = cited_references.copy()

    for i in tqdm(
        range(main_documents.shape[0]),
        total=main_documents.shape[0],
        bar_format="  {percentage:3.2f}% {bar} | {n_fmt}/{total_fmt} [{rate_fmt}] |",
        ascii=" :",
        ncols=73,
    ):
        row = main_documents.iloc[i]
        refs = remaining_references.copy()

        refs = refs.loc[
            refs.key.str.lower().str.contains(row[Field.AUTH_FIRST.value].lower()),
            :,
        ]
        refs = refs.loc[refs.key.str.lower().str.contains(row[Field.YEAR.value]), :]

        refs = refs.loc[
            refs.key.str.lower().str.contains(
                re.escape(row[Field.TITLE_RAW.value][:50].lower())
            ),
            :,
        ]

        if len(refs) > 0:
            mapping[row[Field.RID.value]] = sorted(refs.text.tolist())
            remaining_references = remaining_references.drop(refs.index)

    return mapping


def _get_reverse_mapping(mapping: dict[str, list[str]]) -> dict[str, str]:
    reverse_mapping = {}
    for key, values in mapping.items():
        for value in values:
            reverse_mapping[value] = key
    return reverse_mapping


def _process_references(
    mapping: dict[str, str],
    root_directory: str,
) -> int:

    dataframe = load_main_csv_zip(root_directory=root_directory)
    dataframe[Field.GCR_NORM.value] = dataframe[Field.GCR_RAW.value].copy()
    dataframe[Field.GCR_NORM.value] = dataframe[Field.GCR_NORM.value].str.split(";")
    dataframe[Field.GCR_NORM.value] = dataframe[Field.GCR_NORM.value].apply(
        lambda refs: (
            [y.strip() for y in refs]
            if isinstance(refs, list)
            else refs if isinstance(refs, list) else refs
        ),
    )

    #
    dataframe[Field.GCR_RID.value] = dataframe.apply(
        lambda row: (
            "; ".join(
                f"{mapping.get(ref, '[N/A]')} @ {ref}"
                for ref in row[Field.GCR_NORM.value]
            )
            if isinstance(row[Field.GCR_NORM.value], list)
            else pd.NA
        ),
        axis=1,
    )
    #

    dataframe[Field.GCR_NORM.value] = dataframe[Field.GCR_NORM.value].apply(
        lambda refs: (
            [mapping[ref] for ref in refs if ref in mapping]
            if isinstance(refs, list)
            else refs
        ),
    )
    dataframe[Field.GCR_NORM.value] = dataframe[Field.GCR_NORM.value].str.join("; ")

    save_main_csv_zip(df=dataframe, root_directory=root_directory)

    non_null_count = int(dataframe[Field.GCR_NORM.value].notna().sum())

    return non_null_count


def normalize_global_references(root_directory: str) -> int:

    cited_references = _prepare_cited_references(root_directory=root_directory)
    main_documents = _prepare_main_documents(root_directory=root_directory)
    mapping = _create_mapping(
        main_documents=main_documents, cited_references=cited_references
    )

    reverse_mapping = _get_reverse_mapping(mapping)

    result = _process_references(mapping=reverse_mapping, root_directory=root_directory)
    _create_references_thesaurus_file(root_directory=root_directory)

    return result
