from pathlib import Path

from tm2p.enum.field import Field

from ._renam_col import renam_col

NAMES_TO_TM2 = {
    "AB": Field.ABSTR_RAW.value,  #         → Abstract
    "AD": Field.AFFIL_RAW.value,  #         → Affiliations
    "AID": Field.DOI.value,  #              → DOI / Article Identifier
    "AU": Field.AUTH_RAW.value,  #          → Authors
    "AUID": Field.ORCID.value,  #           → ORCID
    "CI": Field.COPYRIGHT.value,  #         → Copyright
    "CN": Field.CORP_AUTH.value,  #         → Corporate Author
    "COIS": Field.COIS.value,  #            → Conflict of Interest Statement
    "CRDT": Field.CRDT.value,  #            → Creation Date
    "CRF": Field.CRF.value,  #              → Corrected and Republished From
    "CRI": Field.CRI.value,  #              → Corrected and Republished In
    "CTI": Field.CTI.value,  #              → Collective Title
    "DA": Field.DA.value,  #                → Date Created
    "DEP": Field.DEP.value,  #              → Date of Electronic Publication
    "DP": Field.YEAR.value,  #              → Year / Date
    "EDAT": Field.EDAT.value,  #            → Entry Date
    "FAU": Field.AUTH_FULL_NAME.value,  #   → Authors (Full Name)
    "FED": Field.EDITOR.value,  #           → Editors
    "FIR": Field.FIR.value,  #              → Full Investigator Name
    "GR": Field.FUND_DET.value,  #          → Funding Details
    "IRAD": Field.IRAD.value,  #            → Investigator Affiliation
    "IS": Field.ISSN.value,  #              → ISSN
    "JT": Field.SRC_RAW.value,  #           → Source Title
    "LA": Field.LANG.value,  #              → Language of Original Document
    "LID": Field.ART_NO.value,  #              → ART_NO
    "MH": Field.IDXKW_RAW.value,  #         → Index Keywords (controlled vocabulary)
    "MHDA": Field.MHDA.value,  #            → MeSH Date
    "MID": Field.MID.value,  #              → Manuscript ID
    "NI": Field.FUND_TXT.value,  #          → Grant Number
    "OT": Field.AUTHKW_RAW.value,  #        → Author Keywords
    "OTO": Field.OTHER_TERM.value,  #       → Other Terms
    "OWN": Field.OWN.value,  #              → Database Owner
    "PG": Field.PG_FIRST_LAST.value,  #     → Page Start–End
    "PHST": Field.PHST.value,  #            → Publication History
    "PL": Field.PUB_CTRY.value,  #          → Country of Publication
    "PMCID": Field.PMCID.value,  #          → PubMed Central ID
    "PMID": Field.PUBMED.value,  #          → PubMed ID
    "PT": Field.PUBTYPE.value,  #       → Document Type
    "PUBM": Field.PUBLISHER.value,  #       → Publisher
    "RF": Field.N_GCR.value,  #             → Reference Count
    "RIN": Field.RIN.value,  #              → Retraction In
    "RN": Field.CAS_REG_NO.value,  #        → Registry Number
    "SB": Field.SUBJ_SUBSET.value,  #       → Subject Subset
    "SI": Field.SUPPL_INF.value,  #         → Supplement Information
    "SO": Field.SRC_CITATION_INFO.value,  # → Source Title + Citation Info
    "STAT": Field.PUBSTAGE.value,  #        → Publication Status
    "TA": Field.SRC_ISO4_RAW.value,  #      → Source Title (abbreviated)
    "TI": Field.TITLE_RAW.value,  #         → Title
    "TT": Field.TRANSL_TITLE.value,  #      → Translated Title
    "VI": Field.VOL.value,  #               → Volume
}


def s02_renam_pubmed_col(root_directory: str) -> int:

    main_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"
    files_processed = renam_col(main_file, NAMES_TO_TM2)

    return files_processed
