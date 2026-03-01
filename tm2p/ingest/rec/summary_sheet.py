"""
SummarySheet
===============================================================================

Smoke tests:
    >>> from tm2p.explore import SummarySheet
    >>> df = (
    ...     SummarySheet()
    ...     #
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> print(df.to_string(index=True)) # doctest: +SKIP
                                      column  number of records coverage (%)
    0                      source_title_abbr                 50      100.00%
    1                               abstract                 48       96.00%
    2             abstract_nouns_and_phrases                 48       96.00%
    3                           affiliations                 49       98.00%
    4                      author_full_names                 50      100.00%
    5                        author_keywords                 38       76.00%
    6                                authors                 50      100.00%
    7                             authors_id                 50      100.00%
    8              authors_with_affiliations                 49       98.00%
    9                                  coden                 12       24.00%
    10                       conference_code                  3        6.00%
    11                       conference_date                  3        6.00%
    12                   conference_location                  3        6.00%
    13                       conference_name                  3        6.00%
    14                correspondence_address                 34       68.00%
    15                             countries                 49       98.00%
    16                    country_1st_author                 49       98.00%
    17                           db_cited_by                 50      100.00%
    18                               db_main                 50      100.00%
    19                         db_references                 50      100.00%
    20                           descriptors                 50      100.00%
    21                        document_title                 50      100.00%
    22      document_title_nouns_and_phrases                 50      100.00%
    23                         document_type                 50      100.00%
    24                                   doi                 45       90.00%
    25                               editors                  2        4.00%
    26                                   eid                 50      100.00%
    27                       funding_details                 17       34.00%
    28                         funding_texts                 17       34.00%
    29                      global_citations                 50      100.00%
    30                     global_references                 19       38.00%
    31                        index_keywords                 19       38.00%
    32                                  isbn                  3        6.00%
    33                                  issn                 48       96.00%
    34                                 issue                 39       78.00%
    35                              keywords                 42       84.00%
    36                              language                 50      100.00%
    37                                  link                 50      100.00%
    38                       local_citations                 50      100.00%
    39                      local_references                 19       38.00%
    40                     nouns_and_phrases                 50      100.00%
    41                           num_authors                 50      100.00%
    42                           open_access                 25       50.00%
    43               organization_1st_author                 49       98.00%
    44                         organizations                 49       98.00%
    45                            page_count                 43       86.00%
    46                              page_end                 43       86.00%
    47                            page_start                 43       86.00%
    48                     publication_stage                 50      100.00%
    49                             publisher                 50      100.00%
    50                          raw_abstract                 50      100.00%
    51        raw_abstract_nouns_and_phrases                 48       96.00%
    52            raw_abstract_spacy_phrases                  0        0.00%
    53                   author_keywords_raw                 38       76.00%
    54                           raw_authors                 50      100.00%
    55                        raw_authors_id                 50      100.00%
    56                       raw_descriptors                 50      100.00%
    57                    raw_document_title                 50      100.00%
    58  raw_document_title_nouns_and_phrases                 50      100.00%
    59                     raw_document_type                 50      100.00%
    60                 raw_global_references                 49       98.00%
    61                    index_keywords_raw                 19       38.00%
    62                          raw_keywords                 42       84.00%
    63                 raw_nouns_and_phrases                 50      100.00%
    64                      raw_source_title                 50      100.00%
    65                     raw_spacy_phrases                 50      100.00%
    66                  raw_textblob_phrases                 49       98.00%
    67                             record_id                 50      100.00%
    68                             record_no                 50      100.00%
    69                               regions                 49       98.00%
    70                         scopus_art_no                  6       12.00%
    71                                source                 50      100.00%
    72                          source_title                 50      100.00%
    73                              sponsors                  1        2.00%
    74                         subject_areas                 47       94.00%
    75                            subregions                 49       98.00%
    76                    tokenized_abstract                 48       96.00%
    77              tokenized_document_title                 50      100.00%
    78                                volume                 48       96.00%
    79                                  year                 50      100.00%






"""

import pandas as pd  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


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

        report = pd.DataFrame({"column": columns})

        report["number of records"] = [
            n_documents - records[col].isnull().sum() for col in columns
        ]

        report["coverage (%)"] = [
            f"{100*(float(n_documents) - records[col].isnull().sum()) / n_documents:5.2f}%"
            for col in columns
        ]

        return report
