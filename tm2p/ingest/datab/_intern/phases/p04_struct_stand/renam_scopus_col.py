from pathlib import Path

from tm2p.enum.field import Field

from ._renam_col import renam_col

NAMES_TO_TM2 = {
    #
    # A
    #
    "Abbreviated Source Title": Field.SRC_ISO4_RAW.value,
    "Abstract": Field.ABSTR_RAW.value,
    "Acronym": Field.ACRONYM.value,
    "Affiliations": Field.AFFIL_RAW.value,
    "Art. No.": Field.ART_NO.value,
    "Author full names": Field.AUTH_FULL_NAME.value,
    "Author Keywords": Field.AUTHKW_RAW.value,
    "Author(s) ID": Field.AUTHID_RAW.value,
    "Authors with affiliations": Field.AUTH_WITH_AFFIL.value,
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
    "Correspondence Address": Field.CORRESPOND_ADDR.value,
    #
    # D
    #
    "Document Type": Field.DOCTYPE_RAW.value,
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
    "Link": Field.SCOPUS_LINK.value,
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
    "References": Field.GCR_FREE_TEXT.value,
    #
    # S
    #
    "Source title": Field.SRC_RAW.value,
    "Source": Field.DATABASE.value,
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


def renam_scopus_col(root_directory: str) -> int:

    processed_dir = Path(root_directory) / "ingest" / "process"
    main_file = processed_dir / "main.csv.zip"
    ref_file = processed_dir / "ref.csv.zip"

    files_processed = renam_col(main_file, NAMES_TO_TM2)
    files_processed += renam_col(ref_file, NAMES_TO_TM2)

    return files_processed
