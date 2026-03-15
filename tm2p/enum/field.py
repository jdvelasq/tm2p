from enum import Enum


class Field(Enum):

    # -------------------------------------------------------------------------
    # Records
    # -------------------------------------------------------------------------
    REC_NO = "REC_NO"  # Record number
    REC_ID = "REC_ID"  # Record ID
    ART_NO = "ART_NO"  # Record  (Scopus)
    DATABASE = "DATABASE"  # Database (Scopus, WOS, OpenAlex, etc.)

    # ======================================================================= #
    #                                                                         #
    #                         CITATION INFORMATION                            #
    #                                                                         #
    # ======================================================================= #

    # -------------------------------------------------------------------------
    # AUTHORS
    # -------------------------------------------------------------------------

    #
    # Full author name
    #
    AUTH_FULL_NAME = "AUTH_FULL_NAME"

    #
    # Author with affiliations
    #
    AUTH_WITH_AFFIL = "AUTH_WITH_AFFIL"

    #
    # Authors ID
    #
    AUTHID_RAW = "AUTHID_RAW"
    AUTHID_NORM = "AUTHID_NORM"

    #
    # Author name
    #
    AUTH_RAW = "AUTH_RAW"
    AUTH_DISAMB = "AUTH_DISAMB"
    AUTH_NORM = "AUTH_NORM"

    #
    # Author first
    #
    AUTH_FIRST = "AUTH_FIRST"

    #
    # Number of authors
    #
    N_AUTH = "N_AUTH"

    #
    # ORCID
    #
    ORCID = "ORCID"

    #
    # Corporate author
    #
    CORP_AUTH = "CORP_AUTH"

    #
    # Conflict of Interest Statement
    #
    COIS = "COIS"

    # -------------------------------------------------------------------------
    # Document title
    # -------------------------------------------------------------------------
    TITLE_RAW = "TITLE_RAW"
    TITLE_TOK = "TITLE_TOK"
    TITLE_UPPER = "TITLE_UPPER"

    TRANSL_TITLE = "TRANSL_TITLE"

    # -------------------------------------------------------------------------
    # YEAR
    # -------------------------------------------------------------------------
    DATE = "DATE"
    YEAR = "YEAR"

    # -------------------------------------------------------------------------
    # EID
    # -------------------------------------------------------------------------
    EID = "EID"

    # -------------------------------------------------------------------------
    # Source title
    # -------------------------------------------------------------------------
    SRC_RAW = "SRC_RAW"
    SRC_NORM = "SRC_NORM"
    SRC_ID = "SRC_ID"
    SRC_TYPE = "SRC_TYPE"
    SRC_CITATION_INFO = "SRC_CITATION_INFO"

    # -------------------------------------------------------------------------
    # Subject areas
    # -------------------------------------------------------------------------
    ASJC = "ASJC"
    WOS_SC = "WOS_SC"  # Web of Science Subject Categories ~ 256

    # -------------------------------------------------------------------------
    # Volume, issues, pages
    # -------------------------------------------------------------------------
    VOL = "VOL"
    ISSUE = "ISSUE"
    PG_FIRST = "PG_FIRST"
    PG_LAST = "PG_LAST"
    PG_COUNT = "PG_COUNT"
    PG_FIRST_LAST = "PG_FIRST_LAST"

    # -------------------------------------------------------------------------
    # Citation count
    # -------------------------------------------------------------------------
    GCS = "GCS"  # Global citation score
    LCS = "LCS"  # Local citation score
    WOS_Z9 = "WOS_Z9"  # Z9 (number of citations in the last 9 years)
    FWCI = "FWCI"  # OpenAlex Field-Weighted Citation Impact
    WOS_U1 = "WOS_U1"  # Number of citations in the first year after publication
    WOS_U2 = "WOS_U2"  # Number of citations in the second year after publication

    # -------------------------------------------------------------------------
    # Publication information
    # -------------------------------------------------------------------------
    PUBSTAGE = "PUBSTAGE"

    # -------------------------------------------------------------------------
    # DOI
    # -------------------------------------------------------------------------
    DOI = "DOI"

    # -------------------------------------------------------------------------
    # Link
    # -------------------------------------------------------------------------
    SCOPUS_LINK = "SCOPUS_LINK"

    # -------------------------------------------------------------------------
    # Document type
    # -------------------------------------------------------------------------
    DOCTYPE = "DOCTYPE"
    PUBTYPE = "PUBTYPE"
    IS_RETRACTED = "IS_RETRACTED"

    # -------------------------------------------------------------------------
    # Open Access
    # -------------------------------------------------------------------------
    IS_OA = "IS_OA"
    OA = "OA"
    OA_LICENSE = "OA_LICENSE"
    COPYRIGHT = "COPYRIGHT"

    # ======================================================================= #
    #                                                                         #
    #                      BIBLIOGRAPHICAL INFORMATION                        #
    #                                                                         #
    # ======================================================================= #

    # -------------------------------------------------------------------------
    # Affiliations & correspondence address
    # -------------------------------------------------------------------------
    AFFIL_RAW = "AFFIL_RAW"
    CORRESPOND_ADDR = "CORRESPOND_ADDR"
    IS_CORRESPOND = "IS_CORRESPOND"
    EMAIL = "EMAIL"
    CORRESPOND_ORG_ID = "CORRESPOND_ORG_ID"

    #
    # Organization
    #
    ORG_ABBR = "ORG_ABBR"
    ORG_ID = "ORG_ID"
    ORG_NORM = "ORG_NORM"
    ORG_RAW = "ORG_RAW"

    ORG_FIRST = "ORG_FIRST"

    # -------------------------------------------------------------------------
    # Country
    # -------------------------------------------------------------------------
    CTRY = "CTRY"
    CTRY_ISO2 = "CTRY_ISO2"
    CTRY_ISO3 = "CTRY_ISO3"

    CTRY_AFFIL = "CTRY_AFFIL"

    #
    # Country of the first author
    #
    CTRY_FIRST = "CTRY_FIRST"
    CTRY_ISO3_FIRST = "CTRY_ISO3_FIRST"

    # -------------------------------------------------------------------------
    # Region & subregion
    # -------------------------------------------------------------------------
    REGION = "REGION"
    SUBREGION = "SUBREGION"

    # -------------------------------------------------------------------------
    # Serial identifiers
    # -------------------------------------------------------------------------
    ISBN = "ISBN"
    ISSN = "ISSN"
    ISSNE = "ISSNE"
    ISSNP = "ISSNP"

    # -------------------------------------------------------------------------
    # PubMed ID
    # -------------------------------------------------------------------------
    PUBMED = "PUBMED"

    # -------------------------------------------------------------------------
    # Publisher
    # -------------------------------------------------------------------------
    PUBLISHER = "PUBLISHER"  # PU (publisher)
    PUBLISHER_ADDRESS = "PUBLISHER_ADDRESS"
    PUBLISHER_CITY = "PUBLISHER_CITY"

    # -------------------------------------------------------------------------
    # Editor(s)
    # -------------------------------------------------------------------------
    EDITOR = "EDITOR"  # BE (editor)

    # -------------------------------------------------------------------------
    # Language of the original document
    # -------------------------------------------------------------------------
    LANG = "LANG"

    # -------------------------------------------------------------------------
    # Correspondence address
    # -------------------------------------------------------------------------
    CORRESP_ADDR = "CORRESP_ADDR"

    # -------------------------------------------------------------------------
    # Abbreviated source title
    # -------------------------------------------------------------------------
    SRC_ISO4_NORM = "SRC_ISO4_NORM"
    SRC_ISO4_RAW = "SRC_ISO4_RAW"
    SRC_J9 = "SRC_J9"  # J9 (abbreviated source title)

    # ======================================================================= #
    #                                                                         #
    #                           ABSTRACT & KEYWORDS                           #
    #                                                                         #
    # ======================================================================= #

    # -------------------------------------------------------------------------
    # Abstract
    # -------------------------------------------------------------------------
    ABSTR_RAW = "ABSTR_RAW"
    ABSTR_TOK = "ABSTR_TOK"
    ABSTR_UPPER = "ABSTR_UPPER"

    #
    # Abstract acronym
    #
    ABSTR_ACRONYM = "ABSTR_ACRONYM"

    # -------------------------------------------------------------------------
    # Author keywords
    # -------------------------------------------------------------------------
    AUTHKW_RAW = "AUTHKW_RAW"  # DE (author keywords)
    AUTHKW_TOK = "AUTHKW_TOK"
    AUTHKW_NORM = "AUTHKW_NORM"

    # -------------------------------------------------------------------------
    # Index keywords
    # -------------------------------------------------------------------------
    IDXKW_RAW = "IDXKW_RAW"
    IDXKW_TOK = "IDXKW_TOK"
    IDXKW_NORM = "IDXKW_NORM"

    # -------------------------------------------------------------------------
    # Other terms
    # -------------------------------------------------------------------------
    OTHER_TERM = "OTHER_TERM"  # OT (other terms)

    # -------------------------------------------------------------------------
    # Keywords (author + index)
    # -------------------------------------------------------------------------
    KW_TOK = "KW_TOK"
    KW_NORM = "KW_NORM"

    # -------------------------------------------------------------------------
    # Noun phrases
    # -------------------------------------------------------------------------
    NP_TEXTBLOB = "NP_TEXTBLOB"
    NP_SPACY = "NP_SPACY"
    NP_ABSTR_RAW = "NP_ABSTR_RAW"
    NP_TITLE_RAW = "NP_TITLE_RAW"
    NP_RAW = "NP_RAW"

    # -------------------------------------------------------------------------
    # Concepts = keywords + NP
    # -------------------------------------------------------------------------
    CONCEPT_RAW = "CONCEPT_RAW"
    CONCEPT_NORM = "CONCEPT_NORM"
    WORD_RAW = "WORD_RAW"
    WORD_NORM = "WORD_NORM"
    DESCRIPTOR_RAW = "DESCRIPTOR_RAW"

    # ======================================================================= #
    #                                                                         #
    #                             FUNDING DETAILS                             #
    #                                                                         #
    # ======================================================================= #

    # -------------------------------------------------------------------------
    # Acronym
    # -------------------------------------------------------------------------
    ACRONYM = "ACRONYM"

    # -------------------------------------------------------------------------
    # Funding text
    # -------------------------------------------------------------------------
    FUND_DET = "FUND_DET"
    FUND_SPONS = "FUND_SPONS"
    FUND_TXT = "FUND_TXT"

    # ======================================================================= #
    #                                                                         #
    #                            OTHER INFORMATION                            #
    #                                                                         #
    # ======================================================================= #

    # -------------------------------------------------------------------------
    # Tradenames & manufacturers
    # -------------------------------------------------------------------------
    TRADENAME = "TRADENAME"
    MANUFACTURER = "MANUFACTURER"

    # -------------------------------------------------------------------------
    # Accession numbers & chemicals
    # -------------------------------------------------------------------------
    CAS_REG_NO = "CAS_REG_NO"  # CRN (CAS registry number)
    CODEN = "CODEN"  # CD (CODEN)
    SEQ_NO = "SEQ_NO"  # SN (sequence number)

    # -------------------------------------------------------------------------
    # Conference information
    # -------------------------------------------------------------------------
    CONF_CODE = "CONF_CODE"  # CC (conference code)
    CONF_DATE = "CONF_DATE"  # CY
    CONF_LOC = "CONF_LOC"  # CL
    CONF_NAME = "CONF_NAME"  # CN

    # -------------------------------------------------------------------------
    # References
    # -------------------------------------------------------------------------

    #
    # Global cited references
    #
    GCR_FREE_TEXT = "GCR_FREE_TEXT"
    GCR_WOS_FORMAT = "GCR_WOS_FORMAT"
    # GCR_RID = "GCR_RID"

    #
    # Local cited references in WOS format (normalized)
    #
    LCR_NORM = "LCR_WOS_FORMAT"

    #
    # Number of cited references
    #
    N_GCR = "N_GCR"
    N_LCR = "N_LCR"

    # PubMed fields
    PUB_CTRY = "PUB_CTRY"  #       Country of publication
    IRAD = "IRAD"  #               Investigator Affiliation
    CRDT = "CRDT"  #               Creation date
    CRF = "CRF"  #                 Corrected and Republished From
    CRI = "CRI"  #                 Corrected and Republished In
    CTI = "CTI"  #                 Collective Title
    DA = "DA"  #                   Date Created
    DEP = "DEP"  #                 Date of Electronic Publication
    EDAT = "EDAT"  #               Entry Date
    FIR = "FIR"  #                 Full Investigator Name
    MHDA = "MHDA"  #               MeSH Date
    MID = "MID"  #                 Manuscript ID
    OWN = "OWN"  #                 Database Owner
    PHST = "PHST"  #               Publication History
    PMCID = "PMCID"  #             PubMed Central ID
    RIN = "RIN"  #                 Retraction In
    SUPPL_INF = "SUPPL_INF"  #     Supplement Information
    SUBJ_SUBSET = "SUBJ_SUBSET"  # Subject Subset

    # ======================================================================= #
    #                                                                         #
    #                               USER FIELDS                               #
    #                                                                         #
    # ======================================================================= #

    USR0 = "USR0"
    USR1 = "USR1"
    USR2 = "USR2"
    USR3 = "USR3"
    USR4 = "USR4"
    USR5 = "USR5"
    USR6 = "USR6"
    USR7 = "USR7"
    USR8 = "USR8"
    USR9 = "USR9"
