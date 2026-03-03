from pathlib import Path

import pandas as pd  # type: ignore

from tm2p.enum.field import Field

SCOPUS_TO_TM2 = {
    #
    # A
    #
    "Abbreviated Source Title": Field.SRC_ISO4_RAW.value,
    "Abstract": Field.ABSTR_RAW.value,
    "Affiliations": Field.AFFIL_RAW.value,
    "Art. No.": Field.ARN.value,
    "Author full names": Field.AUTH_FULL.value,
    "Author Keywords": Field.AUTHKW_RAW.value,
    "Author(s) ID": Field.AUTHID_RAW.value,
    "Authors with affiliations": Field.AUTHAFFIL.value,
    "Authors": Field.AUTH_RAW.value,
    #
    # C
    #
    "Chemicals/CAS": Field.CAS_REG_NO.value,
    "Cited by": Field.GCS.value,
    "CODEN": Field.CODEN.value,
    "Conference code": Field.CONF_CODE.value,
    "Conference date": Field.CONF_DATE.value,
    "Conference location": Field.CONF_LOC.value,
    "Conference name": Field.CONF_NAME.value,
    "Correspondence Address": Field.CORRESP.value,
    #
    # D
    #
    "Document Type": Field.PUBTYPE_RAW.value,
    "DOI": Field.DOI.value,
    #
    # E
    #
    "Editors": Field.EDITOR.value,
    "EID": Field.EID.value,
    #
    # F
    #
    "Funding Details": Field.FUND_DET.value,
    "Funding Texts": Field.FUND_TXT.value,
    #
    # I
    #
    "Index Keywords": Field.IDXKW_RAW.value,
    "ISBN": Field.ISBN.value,
    "ISSN": Field.ISSN.value,
    "Issue": Field.ISSUE.value,
    #
    # L
    #
    "Language of Original Document": Field.LANG.value,
    "Link": Field.LINK.value,
    #
    # M
    #
    "Manufacturers": Field.MANUFACTURER.value,
    "Molecular Sequence Numbers": Field.SEQ_NO.value,
    #
    # O
    #
    "Open Access": Field.OA.value,
    #
    # P
    #
    "Page count": Field.PG_COUNT.value,
    "Page end": Field.PG_LAST.value,
    "Page start": Field.PG_FIRST.value,
    "Publication Stage": Field.PUBSTAGE.value,
    "Publisher": Field.PUBLISHER.value,
    "PubMed ID": Field.PUBMED.value,
    #
    # R
    #
    "References": Field.REF_RAW.value,
    #
    # S
    #
    "Source title": Field.SRC_RAW.value,
    "Source": Field.DB_SRC.value,
    "Sponsors": Field.FUND_SPONS.value,
    #
    # T
    #
    "Title": Field.TITLE_RAW.value,
    "Tradenames": Field.TRADENAME.value,
    #
    # V
    #
    "Volume": Field.VOL.value,
    #
    # Y
    #
    "Year": Field.YEAR.value,
}


def rename_columns(root_directory: str) -> int:

    processed_dir = Path(root_directory) / "ingest" / "processed"
    main_file = processed_dir / "main.csv.zip"
    references_file = processed_dir / "references.csv.zip"

    files_processed = 0

    for file in [main_file, references_file]:

        if not file.exists():
            continue

        files_processed += 1

        dataframe = pd.read_csv(
            file,
            encoding="utf-8",
            compression="zip",
            low_memory=False,
        )

        dataframe.rename(columns=SCOPUS_TO_TM2, inplace=True)
        mapped_names = set(SCOPUS_TO_TM2.values())
        dataframe.columns = pd.Index(
            [
                (
                    name.lower().replace(".", "").replace(" ", "_")
                    if name not in mapped_names
                    else name
                )
                for name in dataframe.columns
            ]
        )
        temp_file = file.with_suffix(".tmp")
        dataframe.to_csv(
            temp_file,
            sep=",",
            encoding="utf-8",
            index=False,
            compression="zip",
        )
        temp_file.replace(file)

    return files_processed
