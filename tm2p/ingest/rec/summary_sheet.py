"""
SummarySheet
===============================================================================

Smoke tests:
    >>> from tm2p.ingest.rec import SummarySheet
    >>> df = (
    ...     SummarySheet()
    ...     #
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.to_string(index=True))
                 COLUMN  NUM_REC COVERAGE
    0         ABSTR_RAW      180  100.00%
    1         ABSTR_TOK      180  100.00%
    2       ABSTR_UPPER      180  100.00%
    3         AFFIL_RAW      176   97.78%
    4               ARN       69   38.33%
    5              ASJC      108   60.00%
    6         AUTHAFFIL      180  100.00%
    7       AUTHID_NORM      180  100.00%
    8        AUTHID_RAW      180  100.00%
    9       AUTHKW_NORM      154   85.56%
    10       AUTHKW_RAW      154   85.56%
    11       AUTHKW_TOK      154   85.56%
    12      AUTH_DISAMB      180  100.00%
    13       AUTH_FIRST      180  100.00%
    14        AUTH_FULL      180  100.00%
    15        AUTH_NORM      180  100.00%
    16         AUTH_RAW      180  100.00%
    17            CODEN       29   16.11%
    18     CONCEPT_NORM      180  100.00%
    19      CONCEPT_RAW      180  100.00%
    20        CONF_CODE        6    3.33%
    21        CONF_DATE        6    3.33%
    22         CONF_LOC        6    3.33%
    23        CONF_NAME        6    3.33%
    24          CORRESP      141   78.33%
    25             CTRY      180  100.00%
    26       CTRY_FIRST      180  100.00%
    27        CTRY_ISO3      180  100.00%
    28  CTRY_ISO3_FIRST      180  100.00%
    29           DB_SRC      180  100.00%
    30              DOI      169   93.89%
    31           EDITOR        3    1.67%
    32              EID      180  100.00%
    33         FUND_DET       55   30.56%
    34       FUND_SPONS        3    1.67%
    35         FUND_TXT       73   40.56%
    36         GCR_NORM        0    0.00%
    37          GCR_RAW      173   96.11%
    38          GCR_RID      173   96.11%
    39              GCS      180  100.00%
    40       IDXKW_NORM       59   32.78%
    41        IDXKW_RAW       59   32.78%
    42        IDXKW_TOK       59   32.78%
    43             ISBN       23   12.78%
    44             ISSN      146   81.11%
    45            ISSUE      101   56.11%
    46          KW_NORM      162   90.00%
    47           KW_TOK      162   90.00%
    48             LANG      180  100.00%
    49         LCR_NORM        0    0.00%
    50              LCS      180  100.00%
    51             LINK      180  100.00%
    52     NP_ABSTR_RAW      180  100.00%
    53           NP_RAW      180  100.00%
    54         NP_SPACY      180  100.00%
    55      NP_TEXTBLOB      180  100.00%
    56     NP_TITLE_RAW      180  100.00%
    57           N_AUTH      180  100.00%
    58            N_GCR      180  100.00%
    59               OA       66   36.67%
    60              ORG      180  100.00%
    61        ORG_FIRST      180  100.00%
    62         PG_FIRST      114   63.33%
    63          PG_LAST      114   63.33%
    64        PUBLISHER      180  100.00%
    65           PUBMED        2    1.11%
    66         PUBSTAGE      180  100.00%
    67     PUBTYPE_NORM      180  100.00%
    68      PUBTYPE_RAW      180  100.00%
    69           REGION      180  100.00%
    70              RID      180  100.00%
    71              RNO      180  100.00%
    72    SRC_ISO4_NORM      180  100.00%
    73     SRC_ISO4_RAW      180  100.00%
    74         SRC_NORM      180  100.00%
    75          SRC_RAW      180  100.00%
    76        SUBREGION      180  100.00%
    77        TITLE_RAW      180  100.00%
    78        TITLE_TOK      180  100.00%
    79      TITLE_UPPER      180  100.00%
    80             USR0      180  100.00%
    81             USR1      180  100.00%
    82              VOL      164   91.11%
    83             YEAR      180  100.00%





"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.enum.column import COLUMN, COVERAGE, NUM_REC


class SummarySheet(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        records = load_filtered_main_csv_zip(params=self.params)

        #
        # Compute stats per column
        columns = sorted(records.columns)

        n_documents = len(records)

        report = pd.DataFrame({COLUMN: columns})

        report[NUM_REC] = [n_documents - records[col].isnull().sum() for col in columns]

        report[COVERAGE] = [
            f"{100*(float(n_documents) - records[col].isnull().sum()) / n_documents:5.2f}%"
            for col in columns
        ]

        return report
