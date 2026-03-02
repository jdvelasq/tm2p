"""
Main information
===============================================================================

Smoke test:
    >>> from tm2p.discov.overview import MainInformation
    >>> df = (
    ...     MainInformation()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> isinstance(df.index, pd.MultiIndex)
    True
    >>> df.index.names
    FrozenList(['Category', 'Item'])
    >>> len(df) > 0
    True
    >>> 'Value' in df.columns
    True
    >>> df.loc[('GENERAL', 'Documents'), 'Value'] > 0
    True
    >>> df  # doctest: +SKIP
                                                                       Value
    Category       Item
    GENERAL        Annual growth rate %                                51.71
                   Average annual citations per document                8.24
                   Average citations per document                       57.7
                   Average documents per source                         1.16
                   Average references per document                      7.73
                   Documents                                              37
                   Document average age                                10.97
                   Number of sources                                      32
                   Timespan                                        2010:2016
                   Total cited references                                286
    DOCUMENT TYPES Article                                                18
                   Book                                                    5
                   Book chapter                                            2
                   Conference paper                                        8
                   Editorial                                               1
                   Review                                                  2
                   Short survey                                            1
    AUTHORS        Author appearances                                     81
                   Average authors per document                         2.19
                   Average authors per multi-authored documents         2.83
                   Collaboration index                                  2.83
                   Documents per author appearance                      0.46
                   Internationally co-authored documents %             13.51
                   Number of authors                                      72
                   Number of authors of single-authored documents         13
                   Number of multi-authored documents                     24
                   Number of single-authored documents                    13
    AFFILIATIONS   Number of countries                                    22
                   Number of countries (1st author)                       19
                   Number of organizations                                49
                   Number of organizations (1st author)                   30
                   Number of regions                                      18
                   Number of subregions                                   25
    KEYWORDS       Number of author keywords (norm)                       96
                   Number of author keywords (raw)                        97
                   Number of index keywords (norm)                       139
                   Number of index keywords (raw)                        140
                   Number of keywords (norm)                             208
                   Number of keywords (raw)                              211
    NLP            Number of abstract words (raw)                       1584
                   Number of abstract NP phrases (norm)                 1112
                   Number of abstract NP phrases (raw)                  1112
                   Number of NP phrases (norm)                          1176
                   Number of NP phrases (raw)                           1176
                   Number of SpaCy NP phrases                           1233
                   Number of TextBlob NP phrases                         576
                   Number of title NP phrases (norm)                     121
                   Number of title NP phrases (raw)                      121
                   Number of title words (raw)                           202
                   Number of words (raw)                                1615
                   Number of words (norm)                               1615
    KEYWORDS + NLP Number of keywords + NP phrases (norm)               1385
                   Number of keywords + NP phrases (raw)                1385
                   Number of keywords + words (norm)                    1823
                   Number of keywords + words (raw)                     1823





"""

import datetime
from dataclasses import dataclass, field
from typing import Union

import numpy as np
import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip

__reviewed__ = "2026-02-03"


@dataclass
class Stats:
    """:meta private:"""

    category: list = field(default_factory=list)
    item: list = field(default_factory=list)
    value: list = field(default_factory=list)


class MainInformation(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def insert_stats(
        self, stats: Stats, category: str, item: str, value: Union[int, float, str]
    ):
        stats.category.append(category)
        stats.item.append(item)
        stats.value.append(value)
        return stats

    # -------------------------------------------------------------------------
    def count_unique_items(self, dataframe: pd.DataFrame, column: Field) -> int:

        if column.value not in dataframe:
            return 0

        series = dataframe[column.value].copy()
        series = series.dropna()
        series = series.str.split(";")
        series = series.explode()
        series = series.str.strip()
        series = series.drop_duplicates()

        return len(series)

    # -------------------------------------------------------------------------

    def run(self):

        dataframe = load_filtered_main_csv_zip(params=self.params)

        stats = Stats()

        # =====================================================================
        #
        # COMPUTE GENERAL STATS
        #
        # =====================================================================

        def annual_growth_rate():
            n_records = len(dataframe)
            n_years = (
                max(dataframe[Field.YEAR.value]) - min(dataframe[Field.YEAR.value]) + 1
            )
            po = len(
                dataframe[Field.YEAR.value][
                    dataframe[Field.YEAR.value] == min(dataframe[Field.YEAR.value])
                ]
            )
            return round(100 * (np.power(n_records / po, 1 / n_years) - 1), 2)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Annual growth rate %",
            value=annual_growth_rate(),
        )

        # ---------------------------------------------------------------------
        def average_annual_citations_per_document():
            return round(
                dataframe[Field.GCS.value].mean()
                / (
                    dataframe[Field.YEAR.value].max()
                    - dataframe[Field.YEAR.value].min()
                    + 1
                ),
                2,
            )

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Average annual citations per document",
            value=average_annual_citations_per_document(),
        )

        # ---------------------------------------------------------------------
        def average_citations_per_document():
            return round(dataframe[Field.GCS.value].mean(), 2)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Average citations per document",
            value=average_citations_per_document(),
        )

        # ---------------------------------------------------------------------
        def average_documents_per_source():
            sources = dataframe[Field.SRC_RAW.value].copy()
            sources = sources.dropna()
            n_records = len(sources)
            sources = sources.drop_duplicates()
            n_sources = len(sources)
            return round(n_records / n_sources, 2)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Average documents per source",
            value=average_documents_per_source(),
        )

        # ---------------------------------------------------------------------
        def average_references_per_document():
            num_references = dataframe[Field.REF_RAW.value].copy()
            num_references = num_references.dropna()
            num_references = num_references.str.split(";")
            num_references = num_references.map(len)
            return round(num_references.sum() / len(dataframe), 2)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Average references per document",
            value=average_references_per_document(),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Documents",
            value=len(dataframe),
        )

        # ---------------------------------------------------------------------
        def document_average_age():
            mean_years = dataframe[Field.YEAR.value].copy()
            mean_years = mean_years.dropna()
            mean_years = mean_years.mean()
            current_year = datetime.datetime.now().year
            return round(int(current_year) - mean_years, 2)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Document average age",
            value=document_average_age(),
        )

        # ---------------------------------------------------------------------
        def number_of_sources():
            records = dataframe[Field.SRC_RAW.value].copy()
            records = records.dropna()
            records = records.drop_duplicates()
            return len(records)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Number of sources",
            value=number_of_sources(),
        )

        # ---------------------------------------------------------------------
        def timespan():
            return (
                str(min(dataframe[Field.YEAR.value]))
                + ":"
                + str(max(dataframe[Field.YEAR.value]))
            )

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Timespan",
            value=timespan(),
        )

        # ---------------------------------------------------------------------
        def total_cited_references():
            records = dataframe[Field.REF_RAW.value].copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            return len(records)

        stats = self.insert_stats(
            stats,
            category="GENERAL",
            item="Total cited references",
            value=total_cited_references(),
        )

        # =====================================================================
        #
        # COMPUTE "DOCUMENT TYPE" STATS
        #
        # =====================================================================
        def compute_document_type_stats(stats):
            records = dataframe[[Field.PUBTYPE_NORM.value]].dropna()
            document_types_count = (
                records[[Field.PUBTYPE_NORM.value]]
                .groupby(Field.PUBTYPE_NORM.value)
                .size()
            )
            for document_type, count in zip(
                document_types_count.index, document_types_count
            ):
                self.insert_stats(
                    stats,
                    category="DOCUMENT TYPES",
                    item=document_type,
                    value=int(count),  # type: ignore
                )

            return stats

        compute_document_type_stats(stats=stats)

        # =====================================================================
        #
        # COMPUTE AUTHOR STATS
        #
        # =====================================================================

        def author_appearances(data_frame):
            data_frame = data_frame[Field.AUTH_RAW.value].copy()
            data_frame = data_frame.dropna()
            data_frame = data_frame.str.split(";")
            data_frame = data_frame.explode()
            data_frame = data_frame.str.strip()
            return len(data_frame)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Author appearances",
            value=author_appearances(dataframe),
        )

        # ---------------------------------------------------------------------
        def average_authors_per_document(data_frame):
            num_authors = data_frame[Field.N_AUTH.value].dropna()
            return round(num_authors.mean(), 2)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Average authors per document",
            value=average_authors_per_document(dataframe),
        )

        # ---------------------------------------------------------------------
        def average_authors_per_multi_authored_documents(data_frame):
            num_authors = data_frame[data_frame[Field.N_AUTH.value] > 1][
                Field.N_AUTH.value
            ]
            return round(num_authors.mean(), 2)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Average authors per multi-authored documents",
            value=average_authors_per_multi_authored_documents(dataframe),
        )

        # ---------------------------------------------------------------------
        def collaboration_index(data_frame):
            records = data_frame[[Field.AUTH_RAW.value, Field.N_AUTH.value]].dropna()
            records = records[records[Field.N_AUTH.value] > 1]
            n_records = len(records)
            authors = records[Field.AUTH_RAW.value].str.split(";").explode().str.strip()
            n_authors = int(authors.notna().sum())
            return round(n_authors / n_records, 2)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Collaboration index",
            value=collaboration_index(dataframe),
        )

        # ---------------------------------------------------------------------
        def documents_per_author_appearance(data_frame):
            data_frame = data_frame[Field.AUTH_RAW.value].copy()
            data_frame = data_frame.dropna()
            n_records = len(data_frame)
            data_frame = data_frame.str.split(";")
            data_frame = data_frame.explode()
            n_authors = len(data_frame)
            return round(n_records / n_authors, 2)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Documents per author appearance",
            value=documents_per_author_appearance(dataframe),
        )

        # ---------------------------------------------------------------------
        def internationally_co_authored_documents(data_frame):
            countries = data_frame[Field.CTRY.value].copy()
            countries = countries.dropna()
            countries = countries.str.split(";")
            countries = countries.map(len)
            return round(len(countries[countries > 1]) / len(countries) * 100, 2)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Internationally co-authored documents %",
            value=internationally_co_authored_documents(dataframe),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Number of authors",
            value=self.count_unique_items(
                dataframe,
                Field.AUTH_RAW,
            ),
        )

        # ---------------------------------------------------------------------
        def number_of_authors_of_single_authored_documents(data_frame):
            records = data_frame[data_frame[Field.N_AUTH.value] == 1]
            authors = records[Field.AUTH_RAW.value].dropna()
            authors = authors.drop_duplicates()
            return len(authors)

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Number of authors of single-authored documents",
            value=number_of_authors_of_single_authored_documents(dataframe),
        )

        # ---------------------------------------------------------------------
        def number_of_multi_authored_documents(data_frame):
            return len(data_frame[data_frame[Field.N_AUTH.value] > 1])

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Number of multi-authored documents",
            value=number_of_multi_authored_documents(dataframe),
        )

        # ---------------------------------------------------------------------
        def number_of_single_authored_documents(data_frame):
            return len(data_frame[data_frame[Field.N_AUTH.value] == 1])

        stats = self.insert_stats(
            stats,
            category="AUTHORS",
            item="Number of single-authored documents",
            value=number_of_single_authored_documents(dataframe),
        )

        # =====================================================================
        #
        # COMPUTE AFFILIATION STATS
        #
        # =====================================================================

        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of countries",
            value=self.count_unique_items(
                dataframe,
                Field.CTRY,
            ),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of countries (1st author)",
            value=self.count_unique_items(
                dataframe,
                Field.CTRY_FIRST,
            ),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of organizations",
            value=self.count_unique_items(
                dataframe,
                Field.ORG,
            ),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of organizations (1st author)",
            value=self.count_unique_items(
                dataframe,
                Field.ORG_FIRST,
            ),
        )

        # ---------------------------------------------------------------------

        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of regions",
            value=self.count_unique_items(
                dataframe,
                Field.REGION,
            ),
        )

        # ---------------------------------------------------------------------
        stats = self.insert_stats(
            stats,
            category="AFFILIATIONS",
            item="Number of subregions",
            value=self.count_unique_items(
                dataframe,
                Field.SUBREGION,
            ),
        )

        # =====================================================================
        #
        # COMPUTE KEYWORDS STATS
        #
        # =====================================================================

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of author keywords (norm)",
            value=self.count_unique_items(
                dataframe,
                Field.AUTHKW_NORM,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of author keywords (raw)",
            value=self.count_unique_items(
                dataframe,
                Field.AUTHKW_RAW,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of index keywords (norm)",
            value=self.count_unique_items(
                dataframe,
                Field.IDXKW_NORM,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of index keywords (raw)",
            value=self.count_unique_items(
                dataframe,
                Field.IDXKW_RAW,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of keywords (norm)",
            value=self.count_unique_items(
                dataframe,
                Field.KW_NORM,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="KEYWORDS",
            item="Number of keywords (raw)",
            value=self.count_unique_items(
                dataframe,
                Field.KW_TOK,
            ),
        )

        # =====================================================================
        #
        # COMPUTE NLP STATS
        #
        # =====================================================================

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of SpaCy NP phrases",
            value=self.count_unique_items(
                dataframe,
                Field.NP_SPACY,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of TextBlob NP phrases",
            value=self.count_unique_items(
                dataframe,
                Field.NP_TEXTBLOB,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of abstract words (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.ABS_WORD_TOK,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of title words (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.TITLE_WORD_TOK,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of words (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.WORD_TOK,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of abstract NP phrases (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.NP_ABSTR_RAW,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of title NP phrases (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.NP_TITLE_RAW,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of NP phrases (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.NP_RAW,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of keywords + words (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.KEY_AND_WORD_TOK,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of keywords + words (norm)",
            value=self.count_unique_items(
                dataframe,
                Field.KEY_AND_WORD_NORM,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of keywords + NP phrases (tok)",
            value=self.count_unique_items(
                dataframe,
                Field.KW_TOK,
            ),
        )

        stats = self.insert_stats(
            stats,
            category="NLP",
            item="Number of keywords + NP phrases (norm)",
            value=self.count_unique_items(
                dataframe,
                Field.KW_NORM,
            ),
        )

        # =====================================================================
        #
        # REPORT
        #
        # =====================================================================

        frame = pd.DataFrame(
            {
                "Category": stats.category,
                "Item": stats.item,
                "Value": stats.value,
            }
        )
        frame = frame.set_index(["Category", "Item"])

        return frame
