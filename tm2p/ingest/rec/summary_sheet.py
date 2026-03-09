"""
SummarySheet
===============================================================================

Smoke tests:
    >>> from tm2p.ingest.rec import SummarySheet
    >>> df = (
    ...     SummarySheet()
    ...     #
    ...     .where_root_directory("tests/fintech/")
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
    36              GCS      180  100.00%
    37       IDXKW_NORM       59   32.78%
    38        IDXKW_RAW       59   32.78%
    39        IDXKW_TOK       59   32.78%
    40             ISBN       23   12.78%
    41             ISSN      146   81.11%
    42            ISSUE      101   56.11%
    43          KW_NORM      162   90.00%
    44           KW_TOK      162   90.00%
    45             LANG      180  100.00%
    46              LCS      180  100.00%
    47             LINK      180  100.00%
    48     NP_ABSTR_RAW      180  100.00%
    49           NP_RAW      180  100.00%
    50         NP_SPACY      180  100.00%
    51      NP_TEXTBLOB      180  100.00%
    52     NP_TITLE_RAW      180  100.00%
    53           N_AUTH      180  100.00%
    54        N_REF_GBL      180  100.00%
    55               OA       66   36.67%
    56              ORG      180  100.00%
    57        ORG_FIRST      180  100.00%
    58         PG_FIRST      114   63.33%
    59          PG_LAST      114   63.33%
    60        PUBLISHER      180  100.00%
    61           PUBMED        2    1.11%
    62         PUBSTAGE      180  100.00%
    63     PUBTYPE_NORM      180  100.00%
    64      PUBTYPE_RAW      180  100.00%
    65         REF_NORM       97   53.89%
    66          REF_RAW      173   96.11%
    67          REF_RID      173   96.11%
    68           REGION      180  100.00%
    69              RID      180  100.00%
    70              RNO      180  100.00%
    71    SRC_ISO4_NORM      180  100.00%
    72     SRC_ISO4_RAW      180  100.00%
    73         SRC_NORM      180  100.00%
    74          SRC_RAW      180  100.00%
    75        SUBREGION      180  100.00%
    76        TITLE_RAW      180  100.00%
    77        TITLE_TOK      180  100.00%
    78      TITLE_UPPER      180  100.00%
    79             USR0      180  100.00%
    80             USR1      180  100.00%
    81              VOL      164   91.11%
    82             YEAR      180  100.00%






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
