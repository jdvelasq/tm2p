from pathlib import Path

from tm2p.enum.field import Field

from ._renam_col import renam_col

NAMES_TO_TM2 = {
    "AB": Field.ABSTR_RAW.value,
    "AF": Field.AUTH_FULL_NAME.value,
    "AU": Field.AUTH_RAW.value,
    "BE": Field.EDITOR.value,
    "BN": Field.ISBN.value,
    "BP": Field.PG_FIRST.value,
    "C1": Field.AFFIL_RAW.value,
    "CR": Field.GCR_WOS_FORMAT.value,
    "DE": Field.AUTHKW_RAW.value,
    "DI": Field.DOI.value,
    "DT": Field.DOCTYPE_RAW.value,
    "EI": Field.ISSNE.value,
    "EM": Field.EMAIL.value,
    "EP": Field.PG_LAST.value,
    "FU": Field.FUND_DET.value,
    "FX": Field.FUND_TXT.value,
    "ID": Field.IDXKW_RAW.value,
    "IS": Field.ISSUE.value,
    "J9": Field.SRC_J9.value,
    "JI": Field.SRC_ISO4_RAW.value,
    "LA": Field.LANG.value,
    "NR": Field.N_GCR.value,
    "OA": Field.OA.value,
    "OI": Field.ORCID.value,
    "PA": Field.PUBLISHER_ADDRESS.value,
    "PD": Field.DATE.value,
    "PG": Field.PG_COUNT.value,
    "PI": Field.PUBLISHER_CITY.value,
    "PT": Field.PUBTYPE_RAW.value,
    "PU": Field.PUBLISHER.value,
    "PY": Field.YEAR.value,
    "RI": Field.AUTHID_RAW.value,
    "RP": Field.CORRESPOND_ADDR.value,
    "SC": Field.WOS_SC.value,
    "SN": Field.ISSN.value,
    "SO": Field.SRC_RAW.value,
    "TC": Field.GCS.value,
    "TI": Field.TITLE_RAW.value,
    "U1": Field.WOS_U1.value,
    "U2": Field.WOS_U2.value,
    "UT": Field.EID.value,
    "VL": Field.VOL.value,
    "WC": Field.ASJC.value,
    "Z9": Field.WOS_Z9.value,
}


def s02_renam_wos_col(root_directory: str) -> int:

    main_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"
    files_processed = renam_col(main_file, NAMES_TO_TM2)

    return files_processed
