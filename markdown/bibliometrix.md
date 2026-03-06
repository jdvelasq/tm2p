# Comparison of tm2+ with bibliometrix

This is a comparison of "t"m2+: A Python Library for Tech-Mining, Bibliometrics and Science Mapping" with Bibliometrix, based on the most recent (March, 2026) of Bibliometrics

### Interface

Bibliometrix can be used in the command line, or using the Biblioshiny GUI.

tm2+ implements a system of final user-faced classes that are similar to GUIs and wizards in many well-known sofware. In this way, all information for a specific result is stored in a Python file. This is an example:

    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.discov.cross_occur_matrix import Matrix
    >>> df = (
    ...     Matrix()
    ...     #
    ...     # COLUMNS:
    ...     .with_column_field(Field.AUTHKW_TOK)
    ...     .having_column_items_in_top(10)
    ...     .having_column_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_column_item_occurrences_between(None, None)
    ...     .having_column_item_citations_between(None, None)
    ...     .having_column_items_in(None)
    ...     #
    ...     # ROWS:
    ...     .with_index_field(Field.AUTH_NORM)
    ...     .having_index_items_in_top(None)
    ...     .having_index_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_index_item_occurrences_between(2, None)
    ...     .having_index_item_citations_between(None, None)
    ...     .having_index_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )


### Fields for analysis

Bibliometrix uses the following fields for analysis.

- Authors
- Organizations
- Countries
- Sources
- References
- Country of first author
- Organization of first author
- Author Keywords
- Index Keywords
- Keywords

tm2+ extends the set adding:

- Keywords + noun phrases ----> Concepts
- Keywords + words


###  SEARCH / Data / Import or Load 

Bibliometrix allows the user to ingest data from:

* Web of Science
* Scopus
* OpenAlex
* Dimensions
* Lens
* PubMed (.txt format)
* Cochrane (.txt format)


The current version of tm2+ only ingest data from Scopus. For this case, tm2+ uses two primary sources of data: the main database downloaded, and the database of references of the database. This feature allows tm2+ to match references in free-format text with Scopus records. With this input tm2+ is able to transform free-format reference text in a format similar to WoS.


### SEARCH / Data / API

* OpenAlex
* PubMed

Not implemented in tm2+.


### SEARCH / Data / Merge Collections    

Bibliometrix allows the user to merge collections in Excel or R format comming from different DBs.

Not implemented in tm2+.


### SEARCH / Data / Reference Matching

This Bibliometrix tool helps identify and merge duplicate citations in your bibliographic dataset. It uses similarity algorithms to find variants of the same reference, allowing you to clean and standarize your data for more accurate analysis. 

Bibiometrix implements the following distance methods (with similarity threshold between 0.7 and 0.96):

* Jaro-Winkler
* Optimal String Alignment
* Longest Common Subsequence

Bibliometrix allows manual merging of references.

In tm2+, the normalization of cited references follows a procedure conceptually similar to the one implemented in Bibliometrix, but adapted to operate directly on free-text reference strings extracted from Scopus records. After merging the main dataset with the references dataset and applying aggressive text normalization (case folding, accent removal, punctuation stripping), candidate matches are generated using a sequence of approximate filters: (i) year proximit allowing ±1 year, (ii) author similarity based on the Jaro–Winkler metric applied to the first author surname, and (iii) title evidence measured through a high token-recall threshold** over the normalized title words. References passing these filters are grouped under the corresponding record identifier to create a global cited reference thesaurus, which is then used to standardize the cited references field across the corpus. This implementation provides an automated alternative to the manual merging strategy used in Bibliometrix while maintaining robust approximate matching for noisy reference strings. The user can modify and apply this thesaurus to the dataset to modify the references. tm2+ implements a thesaurus system similar to VantagePoint, such that techniques as fuzzy-cutoff matching can be applied to review the thesaurus.


### APPRAISAL / Filters

Bibliometrix implements a complex sequence of filters for selecting records. Biblioshiny uses the following filter options:

* Document type
* Lnaguage
* Publication year
* Subject category (1 or more selected items)
* Journal list
* Bradford law zones
* Region 
* Country
* Global citation range
* Glonal citation per year range

In tm2+, filters are applied per class. This is an example:

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

the methods `where_record_years_range`, `where_record_citations_range`, and `where_records_match` can generate complex filters to select records. Particularly, the last function `where_records_match` receives a python dictionary where the keys are the fields (in a similar way to biblioshiny), and each value is a list of strings with valid values. Records are selected when they match an value in any of the fields sepcified in `where_records_match`.


### ANALYSIS / Overview / Main information

tm2+ generates a pandas dataframe with an similar output to Biblioshiny's main information. This is an example:

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


### ANALYSIS / Overview / Anual scientific production & Average citations per year

tm2+ implements a function to plot several metrics per year, including the number of documents, and the average citations per year.


### ANALYSIS / Overview / Life cycle

Bibliometrix presents a Life Cycle of Scientific Production module that implements a logistic growt model to analyze the temporal dynamics of research topics. This approach, grounded in the theory of scientific paradigms and innovation diffusion, allows researchers to identify the current development stage of a field, predicting future trends, and estimate when a topic reach maturity or saturation. By fitting a logistic curveto the annual publication counts in the data collection, this analysis reveals whether a research are is in its emergence phase, rapid growth phase, maturity phase or decline phase.

Not implemented in tm2+.


### ANALYSIS / Overview / Three-field plot

Bibliometrix implements a three-field plot advanced visualization tool that reveals the relationships among three distinct bibliographic dimensions through an iterative Sankey diagram.

In tm2+, the Sankey plot is implemented for a variable number of fields, not only 3.


### ANALYSIS / Sources / Most relevant sources & Most local cited sources

Bibliometrix presents a table and a diagram with the sources ordened by the number of documents. Also, Bibliometrix presents a table and a diagram with the most local cited sources (in the references) ordened by the number of documents.

tm2+ implements a Metrics class to compute several indicators as is showed in this example:

    >>> from tm2p.anal.metrics import Metrics
    >>> df = (
    ...     Metrics()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
    >>> type(df).__name__
    'DataFrame'
    >>> df.shape[0] > 1
    True
    >>> df.shape[1] > 1
    True
    >>> df.head(10)
                             RANK_OCC  ...                           COUNTERS
    AUTHKW_NORM                        ...
    fintech                         1  ...                  fintech 117:25478
    financial inclusion             2  ...      financial inclusion 017:03823
    financial technology            3  ...     financial technology 014:02508
    green finance                   4  ...            green finance 011:02844
    blockchain                      5  ...               blockchain 011:02023
    banking                         6  ...                  banking 010:02599
    china                           7  ...                    china 009:01947
    innovation                      8  ...               innovation 009:01703
    artificial intelligence         9  ...  artificial intelligence 008:01915
    financial services             10  ...       financial services 007:01673
    <BLANKLINE>
    [10 rows x 17 columns]
    >>> from pprint import pprint
    >>> pprint(df.columns.tolist())
    ['RANK_OCC',
     'RANK_GCS',
     'RANK_LCS',
     'OCC',
     'GCS',
     'LCS',
     'YEAR_FIRST',
     'YEAR_LAST',
     'AGE',
     'GCS_PER_YEAR',
     'LCS_PER_YEAR',
     'GCS_PER_DOC',
     'LCS_PER_DOC',
     'H_INDEX',
     'G_INDEX',
     'M_INDEX',
     'COUNTERS']


These metrics can be presented using a:

* Bar plot (horizontal bars)
* Cleveland dot plot
* Column plot (vertical bars)
* Line plot
* Pie plot
* Word cloud

The class Metrics can be applied to any of the fields already listed.


### ANALYSIS / Sources / Bradford's Law

Bibliometrix presents a plot and a table with the following information:

* Source
* Rank
* Freq
* cumFreq
* Zone

tm2+ implements a class with a similar output.

### ANALYSIS / Sources / Local impact

Bibliometrix presents a bar plot and a table with the following impact measures:

* H-index
* G-index
* M-index
* Total citation

Already considered in the class Metrics.


### ANALYSIS / Sources / Production over time

Bibliometrix present a line plot with the cummulative occurrences by most frequent sources, and a table with:

* The sources in the colums
* The years in the rows
* The number of documents per source per year

tm2+, for any of the available fields, uses the class Trends to generate a pandas dataframe with the occurrences per year per item. item corresponds to the values in any analyzed field.


### ANALYSIS / Authors / Author profile

Bibliometrix presents:

* Global author profile obtained from OpenAlex
* Local author profile obtained from the current dataset

tm2+ not implement this feature.


### ANALYSIS / Authors / Most relevant authors

Bibliometrix presents a plot a table with the authors sorted by the number of documents in the database.

Already considered in Metrics class.

### ANALYSIS / Authors / Most local cited authors

Bibliometrix presents a plot and table with the most local cited authors.

tm2+ computed the Local Citation Score as part of Metrics class output.


### ANALYSIS / Authors / Author's production over time

The bibliometrix table contains:

* Author
* Year
* Freq
* TC
* TCpY

Already considered in Trends class.


### ANALYSIS / Authors / Lotka's law

Bibliomeetrix table contains:

* Documents written
* No of authors
* Proportion of authors
* Theorethical

Implemented in tm2+.


### ANALYSIS / Authors / Author's local impact

Bibliometrix uses the following impact measures:

* H-index
* M-index
* G-index
* Total citations

Also implemented in Metrics.


### ANALYSIS / Affiliations / Most relevant affiliations

Plot and table of the number of documents per affiliation

Also implemented in Metrics.


### ANALYSIS / Affiliations / Affiliations production over time

Bibliometrix presents a cumulative number of documents per year. The corresponding table has:

* Affiliation
* Year
* Num articles

Also implemented in Metrics.


### ANALYSIS / Countries / Corresponding author's country

Bibliometrics presents a table and bar plot with MCP (multi-country publication and single-country publication). The table contains:

* Country
* Articles
* Articles %
* SCP
* MCP
* MCP %

Implemented in tm2+.


### ANALYSIS / Countries / Countries' scientific production

Bibliometrix's worldmap with the number of documents per country. 

Implemented in tm2+. It is a class using Metrics and CTRY as field.


### ANALYSIS / Countries / Countries production over time

Line plot with the cummulative number of documents per year for the most frequent countries.

Implemented in tm2+. 


### ANALYSIS / Countries / Most cited countries

Bar plot and table with the citations per country

Also implemented in Metrics.


### ANALYSIS / Documents / Most global cited documents

Bar plot and table with the most cited records in the database.

Also implemented in Metrics.


### ANALYSIS / Documents / Most local cited documents

Bar plot and table with the most cited records in the database.

Also implemented in Metrics.


### ANALYSIS / Cited references / Most local cited references



### ANALYSIS / Cited references / RPYS

Also implemented.


### ANALYSIS / Words / Most cited words

Implemented for:

* Author keywords
* Index keywords
* All keywords
* Titles
* Abstracts
* Subject categories (WoS)

Also implemented in Metrics.

### ANALYSIS / Words / WordCloud

Also implemented in Metrics.

### ANALYSIS / Words / Treemap

Also implemented in Metrics.

### ANALYSIS / Words / Word's frequency over time

Cumulative occurrences. Implemented in Trends


### ANALYSIS / Words / Trend topics

Also implemented in tm2+.


### SYNTHESIS / Clustering by coupling

Unit of analysis: 

* Documents
* Authors
* Sources

Coupling by:

* References
* Keywords
* Author keywords
* Index keywords
* Titles
* Abstracts

The outputs are:

* Centrality-impact diagram
* Coupling network
* Table of documents/authors/sources by cluster


tm2+ implements document coupling.


### SYNTHESIS / Co-occurrence network

Bibliometrix produces the following output:

* Network
* Diachonich network (animation)
* Density
* Table
* Degree plot

Implemented in tm2+.


### SYNTHESIS / Thematic map

* Density-Centrality plot
* Network
* Table
* Clusters
* Documents

Not implemented


### SYNTHESIS / Thematic evolution

Not implemented


### SYNTHESIS / Factorial approach

Implements:
* Correspondece analysis
* Multiple correspondence analysis
* Multidimensional scaling

For:
* Word map
* Topic dendogram
* Words by cluster
* Docs by cluster

Not implemented.


### SYNTHESIS / Intelletual structure / co-citation network

* Network
* Density
* Table
* Degree plot

Implemented in tm2+.


### SYNTHESIS / Intelectual structure / Collaboration network

For authors, institutions and countries.

Implemented in tm2+.


### SYNTHESIS / Intelectual structure / Country collaboration world map

Implemented in tm2+.

