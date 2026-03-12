import re
import unicodedata
from pathlib import Path

import Levenshtein  # type: ignore
import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import (
    load_main_csv_zip,
    load_references_csv_zip,
    save_main_csv_zip,
)

AUTH_FIRST = Field.AUTH_FIRST.value
AUTH_RAW = Field.AUTH_RAW.value
GCR_NORM = Field.GCR_WOS_FORMAT.value
GCR_RAW = Field.GCR_FREE_TEXT.value
RID = Field.RID.value
SRC = Field.SRC_RAW.value
TITLE = Field.TITLE_RAW.value
YEAR = Field.YEAR.value

SELECTED_FIELDS = [
    RID,
    TITLE,
    AUTH_RAW,
    YEAR,
    SRC,
]


def normalize_global_references(root_directory: str) -> int:

    mapping = _generate_gcr_thesaurus_file(root_directory=root_directory)
    result = _process_references(mapping=mapping, root_directory=root_directory)

    return result


def _generate_gcr_thesaurus_file(root_directory: str) -> dict[str, list[str]]:

    merged = _merge_csv_zip_files(root_directory=root_directory)
    formated = _format_merged(df=merged)
    references = _get_cited_references(root_directory=root_directory)
    mapping = _create_mapping(formated=formated, references=references)

    _save_thesaurus_file(mapping=mapping, root_directory=root_directory)

    return mapping


def _merge_csv_zip_files(root_directory: str) -> pd.DataFrame:

    main_df = load_main_csv_zip(root_directory=root_directory)
    main_df = main_df[SELECTED_FIELDS].dropna()

    ref_df = load_references_csv_zip(root_directory=root_directory)

    if ref_df.empty:
        main_df = main_df.sort_values(by=[Field.RID.value])  # type: ignore
        return main_df  # type: ignore

    ref_df = ref_df[SELECTED_FIELDS].dropna()

    merged_df = pd.concat([main_df, ref_df], axis=0)
    merged_df = merged_df.drop_duplicates()
    merged_df = merged_df.sort_values(by=[Field.RID.value])  # type: ignore

    return merged_df


def _format_merged(df: pd.DataFrame) -> pd.DataFrame:

    df[AUTH_FIRST] = df[AUTH_RAW].apply(_extract_first_author_surname)
    df[TITLE] = df[TITLE].apply(_format_text)
    df[YEAR] = df[YEAR].astype(str)
    df = df.sort_values(by=[RID])  # type: ignore

    return df


def _extract_first_author_surname(authors: str) -> str:
    surname = authors.split(" ")[0]
    surname = surname.lower()
    surname = surname.replace(",", "")
    surname = unicodedata.normalize("NFD", surname)
    surname = surname.encode("ascii", "ignore").decode("utf-8")
    return surname


def _format_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = text.lower()
    text = re.sub(r"[.,:;()\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _get_cited_references(root_directory: str) -> pd.DataFrame:

    references = load_main_csv_zip(root_directory=root_directory)
    references = references[[GCR_RAW]].copy()
    references = references.dropna()
    references = references.rename(columns={GCR_RAW: "text"})  # type: ignore

    references["text"] = references["text"].str.split(";")
    references = references.explode("text")
    references["text"] = references["text"].str.strip()
    references = references.drop_duplicates()
    references = references.reset_index(drop=True).copy()

    references["key"] = references["text"].apply(_format_text)

    return references


def _create_mapping(
    formated: pd.DataFrame,
    references: pd.DataFrame,
) -> dict[str, list[str]]:

    mapping = {}
    remaining_references = references.copy()

    for i in tqdm(
        range(formated.shape[0]),
        total=formated.shape[0],
        bar_format="  {percentage:3.2f}% {bar} | {n_fmt}/{total_fmt} [{rate_fmt}] |",
        ascii=" :",
        ncols=73,
    ):
        row = formated.iloc[i]
        refs = remaining_references.copy()
        refs = _keep_refs_with_approx_year_match(refs, row[YEAR])
        refs = _keep_refs_with_approx_author_match(refs, row[AUTH_FIRST])
        refs = _keep_refs_with_approx_title_match(refs, row[TITLE])

        if len(refs) > 0:
            mapping[row[RID]] = sorted(refs.text.tolist())
            remaining_references = remaining_references.drop(refs.index)

    return mapping


def _keep_refs_with_approx_year_match(refs, year):
    year_before = str(int(year) - 1)
    year_after = str(int(year) + 1)
    refs = refs.copy()
    refs = refs.loc[
        refs.key.str.lower().str.contains(year)
        | refs.key.str.lower().str.contains(year_before)
        | refs.key.str.lower().str.contains(year_after),
        :,
    ]
    return refs


def _keep_refs_with_approx_author_match(refs, surname):

    def jaro_winkler(text):
        words = text.split()
        words = words[:3]
        metric = max(Levenshtein.jaro_winkler(surname, word) for word in words)
        return metric >= 0.95

    refs = refs.copy()
    refs = refs.loc[refs.key.apply(jaro_winkler), :]
    return refs


def _keep_refs_with_approx_title_match(refs, title):

    def compute_token_recall(text):
        counter = 0
        for word in title_words:
            if word in text:
                counter += 1
        return counter / len(title_words) >= 0.85

    title_words = title.split()
    refs = refs.copy()
    refs = refs.loc[refs.key.apply(compute_token_recall), :]
    return refs


def _get_reverse_mapping(mapping: dict[str, list[str]]) -> dict[str, str]:
    reverse_mapping = {}
    for key, values in mapping.items():
        for value in values:
            reverse_mapping[value] = key
    return reverse_mapping


def _save_thesaurus_file(mapping: dict[str, list[str]], root_directory: str) -> None:

    filepath1 = Path(root_directory) / "refine" / "thesaurus" / "gcr.the.txt"
    filepath2 = Path(root_directory) / "ingest" / "process" / "_gcr.the.txt"

    for filepath in [filepath1, filepath2]:

        with open(filepath, "w", encoding="utf-8") as file:
            for key, values in mapping.items():
                file.write(f"{key}\n")
                for value in values:
                    file.write(f"    {value}\n")


def _process_references(
    mapping: dict[str, list[str]],
    root_directory: str,
) -> int:

    rev_mapping = _get_reverse_mapping(mapping)

    dataframe = load_main_csv_zip(root_directory=root_directory)
    dataframe[GCR_NORM] = dataframe[GCR_RAW].copy()
    dataframe[GCR_NORM] = dataframe[GCR_NORM].str.split(";")
    dataframe[GCR_NORM] = dataframe[GCR_NORM].apply(
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
                f"{rev_mapping.get(ref, '[N/A]')} @ {ref}" for ref in row[GCR_NORM]
            )
            if isinstance(row[GCR_NORM], list)
            else pd.NA
        ),
        axis=1,
    )
    #

    dataframe[GCR_NORM] = dataframe[GCR_NORM].apply(
        lambda refs: (
            [mapping[ref] for ref in refs if ref in mapping]
            if isinstance(refs, list)
            else refs
        ),
    )
    dataframe[GCR_NORM] = dataframe[GCR_NORM].str.join("; ")

    save_main_csv_zip(df=dataframe, root_directory=root_directory)

    non_null_count = int(dataframe[GCR_NORM].notna().sum())

    return non_null_count


# ------


# def _clean_text(text):
#     """:meta private:"""
#     text = (
#         text.str.lower()
#         .str.replace(".", "", regex=False)
#         .str.replace(",", "", regex=False)
#         .str.replace(":", "", regex=False)
#         .str.replace("-", " ", regex=False)
#         .str.replace("_", " ", regex=False)
#         .str.replace("'", "", regex=False)
#         .str.replace("(", "", regex=False)
#         .str.replace(")", "", regex=False)
#         .str.replace("  ", " ", regex=False)
#     )
#     return text


# def _prepare_main_documents(root_directory: str) -> pd.DataFrame:

#     main_docs = load_main_csv_zip(root_directory=root_directory)

#     main_docs = main_docs[SELECTED_FIELDS]
#     main_docs = main_docs.dropna()
#     references_path = get_references_csv_zip_path(root_directory)
#     if references_path.exists():
#         references_df = load_references_csv_zip(root_directory=root_directory)
#         references_df = references_df[SELECTED_FIELDS].dropna()
#         dataframe = pd.concat([main_docs, references_df], axis=0)
#         dataframe = dataframe.drop_duplicates()
#     else:
#         dataframe = main_docs

#     dataframe[Field.AUTH_FIRST.value] = (
#         dataframe[Field.AUTH_RAW.value]
#         .str.split(" ")
#         .map(lambda x: x[0].lower().replace(",", ""))
#     )
#     dataframe[Field.TITLE_RAW.value] = dataframe[Field.TITLE_RAW.value].str.lower()
#     dataframe[Field.TITLE_RAW.value] = _clean_text(dataframe[Field.TITLE_RAW.value])
#     dataframe[Field.AUTH_RAW.value] = _clean_text(dataframe[Field.AUTH_RAW.value])
#     dataframe[Field.YEAR.value] = dataframe[Field.YEAR.value].astype(str)
#     dataframe = dataframe.sort_values(by=[Field.RID.value])  # type: ignore

#     return dataframe


# def _create_references_thesaurus_file(root_directory: str) -> None:

#     dataframe = load_main_csv_zip(root_directory=root_directory)
#     dataframe = dataframe[[Field.GCR_RID.value]].copy().dropna()
#     dataframe[Field.GCR_RID.value] = dataframe[Field.GCR_RID.value].str.split("; ")
#     dataframe = dataframe.explode(Field.GCR_RID.value)  # type: ignore
#     dataframe[Field.GCR_RID.value] = dataframe[Field.GCR_RID.value].str.strip()
#     dataframe["rec_id"] = dataframe[Field.GCR_RID.value].apply(
#         lambda x: x.split(" @ ")[0].strip() if " @ " in x else "[n/a]"
#     )
#     dataframe["ref"] = dataframe[Field.GCR_RID.value].apply(
#         lambda x: x.split(" @ ")[1].strip() if " @ " in x else "[n/a]"
#     )

#     # counting = dataframe["ref"].value_counts()
#     # dataframe["ref"] = dataframe["ref"].apply(
#     #     lambda x: f"{x} # occ: {counting.get(x, 0)}"
#     # )

#     dataframe = dataframe[["rec_id", "ref"]]
#     groupby_df = dataframe.groupby("rec_id", as_index=False).agg({"ref": list})
#     groupby_df["ref"] = groupby_df["ref"].apply(sorted)
#     groupby_df = groupby_df.sort_values(by=["rec_id"], ascending=True)

#     filepath = Path(root_directory) / "refine" / "thesaurus" / "gcr.the.txt"

#     with open(filepath, "w", encoding="utf-8") as file:
#         for _, row in groupby_df.iterrows():
#             rec_id = row["rec_id"]
#             if rec_id == "[n/a]":
#                 continue
#             file.write(f"{rec_id}\n")
#             for ref in row["ref"]:
#                 file.write(f"    {ref}\n")
