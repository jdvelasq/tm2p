#!/usr/bin/env python3
"""
tech_mining_benchmark.py
─────────────────────────────────────────────────────────────────────────────
Prints a SAS-style horizontal bar chart comparing tech-mining / bibliometrics /
scientometrics software against a notional gold standard (score = 100).

Parity score = features implemented by a tool / total features × 100

The feature surface and all competitor scores are hard-coded in this file.
Only tm2+ is dynamic: its score is recomputed each run from a YAML file
that records which features have been implemented.

Usage:
    python tech_mining_benchmark.py [path/to/tm2plus.yaml] [--table]

    --table   also prints the full feature matrix at the end

If the YAML path is omitted the script looks for tm2plus.yaml in the
current directory.  If no YAML file is found, a ready-to-fill template is
generated automatically.

YAML format (flat dict of feature-id -> bool):
    features:
      wos_import:    true
      scopus_import: true
      pubmed_import: false
      ...
"""

import sys
from datetime import date
from itertools import groupby
from pathlib import Path

import yaml

# ═══════════════════════════════════════════════════════════════════════════════
#  EMBEDDED FEATURE DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

FEATURES: list[dict] = [
    # ── Data Import & Sources ─────────────────────────────────────────────────
    dict(
        id="import_wos",
        name="WoS Import",
        description="Import records exported from Web of Science in tab-delimited (.txt) or BibTeX format. Supports full-record exports including author keywords, index keywords, references, abstracts, subject categories, and times-cited counts. Implemented by: VOSviewer, CiteSpace, Bibliometrix, SciMAT, CoPalRed, HistCite, ScientoPy.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=True,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="import_scopus",
        name="Scopus Import",
        description="Import records exported from Scopus in CSV (Excel-compatible) format. Supports document metadata, author affiliations, keywords, abstract, and cited-by count. Bibliometrix additionally accepts Scopus BibTeX export. CITAN reads Scopus CSV exports directly into its local bibliometric storage. Implemented by: VOSviewer, CiteSpace, Bibliometrix, SciMAT, CoPalRed, ScientoPy, CITAN.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="import_openalex",
        name="OpenAlex Import / API",
        description="Import bibliographic records from the OpenAlex open scholarly graph, either by reading a downloaded file or by querying the live REST API with filters. Provides access to hundreds of millions of works with open metadata including concepts, institutions, and citation counts. Implemented by: Bibliometrix (file + API).",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="import_pubmed",
        name="PubMed Import / API",
        description="Import records from PubMed / MEDLINE in .txt (PubMed tagged format) or via the Entrez API. Provides access to biomedical literature with MeSH terms, abstracts, and citation data. Bibliometrix also supports PubMed API; VOSviewer and CiteSpace accept PubMed exports. Implemented by: VOSviewer, CiteSpace, Bibliometrix.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="import_dimensions",
        name="Dimensions Import",
        description="Import records exported from the Dimensions database in CSV or Export-for-bibliometric-mapping format. Dimensions covers a broader literature than WoS/Scopus including book chapters, preprints, and datasets. Provides citation counts, Altmetric scores, and funding information. Implemented by: VOSviewer, Bibliometrix.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="import_lens",
        name="Lens.org Import",
        description="Import records exported from Lens.org in CSV or JSON format. Lens.org is a free open scholarly database integrating PubMed, Crossref, and patent literature. Provides DOIs, abstracts, and citation data. Implemented by: Bibliometrix.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="import_cochrane",
        name="Cochrane Import",
        description="Import records from the Cochrane Library in .txt export format. Cochrane specialises in systematic reviews and clinical trials. Provides structured abstracts, MeSH terms, and review metadata. Implemented by: Bibliometrix.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="merge_collections",
        name="Merge Collections",
        description="Merge bibliographic collections downloaded from different databases (e.g. WoS + Scopus + Dimensions) into a single unified dataset. VOSviewer accepts multiple database files simultaneously in the Create Map wizard. Bibliometrix merges collections in R/Excel format. ScientoPy merges WoS and Scopus exports. Implemented by: VOSviewer, Bibliometrix, ScientoPy.",
        category="Data Import & Sources",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    # ── Data Cleaning & Normalization ─────────────────────────────────────────
    dict(
        id="reference_matching",
        name="Reference Matching / Deduplication",
        description="Identify and merge variant forms of the same cited reference within the corpus reference lists using fuzzy string similarity (Jaro-Winkler, Optimal String Alignment, Longest Common Subsequence). Bibliometrix applies configurable similarity thresholds (0.70-0.96) and supports manual merging. The result is a global cited-reference thesaurus that standardises the references field across all records. Implemented by: Bibliometrix.",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="thesaurus",
        name="Thesaurus / Term Normalization",
        description="Apply a user-editable thesaurus file to replace variant forms of keywords, author names, organisation names, country names, cited references, or terms with a single canonical form before analysis. VOSviewer supports thesaurus files (label/replace-by columns) for both bibliographic data and text data, including term ignoring. CoPalRed implements thesaurus-based normalisation as a core preprocessing step. Implemented by: VOSviewer, CoPalRed.",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="deduplication",
        name="Duplicate Record Removal",
        description="Automatically detect and remove duplicate document records across the imported dataset. Matching uses a combination of DOI equality and normalised title + first-author last-name similarity (case-folded, accent-stripped, punctuation-removed). When duplicates are found, times-cited counts are averaged across the merged records. CoPalRed relies on thesaurus-based normalisation and does not perform automatic duplicate detection by DOI/title matching. CITAN provides fuzzy duplicate-title detection with configurable aggressiveness and a GUI dialog for manual confirmation and removal. Implemented by: VOSviewer, CiteSpace, Bibliometrix, SciMAT, ScientoPy, CITAN.",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="author_normalization",
        name="Author Name Normalization",
        description="Normalise author name representations to ensure cross-database and cross-record author identity consistency. Normalisation steps include: accent removal, separator standardisation (comma, semicolon, pipe), dot stripping from initials, and case folding. Without this step the same author may appear under multiple distinct name strings, inflating author counts and distorting co-authorship networks. CITAN provides a fuzzy duplicate-author detection function with a GUI dialog for selecting and merging author groups. Implemented by: Bibliometrix, ScientoPy, CITAN.",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="country_normalization",
        name="Country Name Normalization",
        description="Standardise country name variants to a single canonical form using a replacement table. Common examples: 'USA' and 'U.S.A.' become 'United States', 'Peoples R China' becomes 'China', 'England' becomes 'United Kingdom'. Without normalisation a single country may appear as multiple distinct values, fragmenting country-level analysis and maps. ScientoPy ships a built-in replacement table; Bibliometrix applies similar normalisation in its preprocessing pipeline. Implemented by: CiteSpace, Bibliometrix, ScientoPy.",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="institution_extract",
        name="Institution Extraction from Affiliations",
        description="Extract institution (affiliation) names from the raw author-affiliation field of imported records and associate them with each document. WoS records store affiliations in the structured C1 field; Scopus uses a separate affiliation column. Extracted institution strings are then normalised and used as the source for institution-level metrics, collaboration networks, and production-over-time analyses. Implemented by: CiteSpace, Bibliometrix, ScientoPy (WoS-sourced records).",
        category="Data Cleaning & Normalization",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    # ── Filtering & Record Selection ──────────────────────────────────────────
    dict(
        id="filter_doctype",
        name="Filter by Document Type",
        description="Filter the active corpus to retain only records of specified document types. Typical types: Article, Review, Conference Paper, Book Chapter, Editorial, Letter. ScientoPy by default keeps Article, Review, Conference Paper, Proceedings, and Article in Press, discarding the rest. Biblioshiny exposes this as a multi-select control. Applied before all downstream analyses. Implemented by: CiteSpace, Bibliometrix, SciMAT, CoPalRed, ScientoPy.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="filter_year",
        name="Filter by Year Range",
        description="Restrict the active corpus to records published within a specified year range (startYear to endYear). ScientoPy exposes --startYear and --endYear CLI parameters. Biblioshiny provides a slider. SciMAT, CiteSpace, and CoPalRed all support year-range filtering. All subsequent analyses operate only on the filtered subset. Implemented by: CiteSpace, Bibliometrix, SciMAT, CoPalRed, ScientoPy.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_citations",
        name="Filter by Citation Range",
        description="Filter records by a minimum or maximum global citation count range. Allows the user to focus analysis on highly cited papers (e.g. top-100 most cited) or to exclude uncited records from network and trend analyses. Bibliometrix exposes this as a numeric range control in Biblioshiny and via its R API. Implemented by: Bibliometrix.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_field",
        name="Filter by Field Value",
        description="Filter records by matching arbitrary field values: journal list, subject category, specific keywords, country, language, or any other metadata field. Biblioshiny provides a multi-select control per field. ScientoPy uses the --criterion parameter to select the analysis field and filters by the given topic list. Bibliometrix also supports compound field filtering via its R API. Implemented by: CiteSpace, Bibliometrix, SciMAT, CoPalRed, ScientoPy.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_bradford",
        name="Filter by Bradford Zone",
        description="Filter records to retain only those published in sources belonging to a specific Bradford Law zone (core zone 1, zone 2, or periphery zone 3). Bradford's Law partitions journals by their cumulative contribution to a research field: zone 1 contains the small core of highly productive journals. Filtering to zone 1 gives a focused high-quality corpus. Implemented by: Bibliometrix.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_language",
        name="Filter by Language",
        description="Filter the corpus to retain only records written in one or more selected languages (e.g. English only, or English and Spanish). Language information is taken from the language field of the imported records (WoS LA field, Scopus Language column). Applied as a preprocessing step before all analyses. Implemented by: Bibliometrix.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_region",
        name="Filter by Region / Country",
        description="Filter the corpus to retain only records whose corresponding or first author is affiliated with institutions in selected regions or countries. Biblioshiny exposes region and country as separate multi-select filter controls. Requires prior country normalisation to be effective. Implemented by: Bibliometrix.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="filter_subject",
        name="Filter by Subject Category",
        description="Filter records by WoS subject category or Scopus ASJC subject area code. Allows the user to restrict a multi-disciplinary export to a single discipline (e.g. Computer Science or Engineering). ScientoPy supports subject as a --criterion value (WoS SC field). Bibliometrix and SciMAT expose it as a multi-select control in their GUIs. Implemented by: CiteSpace, Bibliometrix, SciMAT, ScientoPy.",
        category="Filtering & Record Selection",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    # ── Descriptive Overview ──────────────────────────────────────────────────
    dict(
        id="preprocessing_report",
        name="Preprocessing Summary Report",
        description="Produce a preprocessing summary graph and table after data loading and cleaning. Reports: total records loaded per database, records omitted by document-type filter, duplicate records removed, and final record count used for analysis. ScientoPy generates this automatically at the end of its preprocessing step. Bibliometrix provides equivalent counts within the main information table. Implemented by: Bibliometrix, ScientoPy.",
        category="Descriptive Overview",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="main_info",
        name="Main Information Summary",
        description="Produce a comprehensive summary statistics table for the entire corpus. Fields: timespan, number of sources, documents, annual growth rate, document average age, average citations per document, average references per document, number of authors, collaboration index (average authors per multi-authored document), number of author keywords and index keywords, number of countries, affiliations, and document type breakdown. Bibliometrix additionally reports NLP-derived phrase counts when noun-phrase extraction is active. Implemented by: CiteSpace, Bibliometrix, SciMAT, HistCite.",
        category="Descriptive Overview",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=False,
            CITAN=True,
        ),
    ),
    dict(
        id="annual_production",
        name="Annual Scientific Production",
        description="Plot and table of the number of documents and average citations per year over the corpus timespan. Visualises the growth trajectory of a research field. Bibliometrix and SciMAT produce bar/line plots with dual axes (documents left, citations right). ScientoPy produces a time-line graph per criterion value. HistCite plots yearly document and citation counts as bar charts. Implemented by: CiteSpace, Bibliometrix, SciMAT, HistCite, ScientoPy.",
        category="Descriptive Overview",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="life_cycle",
        name="Life Cycle / Logistic Growth Model",
        description="Fit a logistic growth (S-curve) model to the annual publication count time series to characterise the development stage of a research field. The model estimates the inflection point, the saturation level, and the current phase: emergence (early exponential), rapid growth (pre-inflection), maturity (post-inflection), or decline (saturation). Output includes the fitted curve overlaid on the observed data and a phase classification label. Grounded in the theory of scientific paradigms and innovation diffusion. Implemented by: Bibliometrix.",
        category="Descriptive Overview",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="sankey",
        name="Sankey / Three-field Plot",
        description="Visualise relationships among multiple bibliographic dimensions simultaneously using a Sankey (alluvial) diagram. Bibliometrix calls this the three-field plot, connecting three user-selected fields (e.g. authors, keywords, journals) as parallel columns with flow ribbons proportional to co-occurrence counts. tm2+ generalises this to any number of fields. Useful for detecting structural patterns between authors, topics, and publication venues. Implemented by: Bibliometrix.",
        category="Descriptive Overview",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Source / Journal Analysis ─────────────────────────────────────────────
    dict(
        id="source_metrics",
        name="Source Metrics (Most Relevant Sources)",
        description="Rank journals and other publication sources by bibliometric indicators computed from the corpus. Indicators include: number of documents (OCC), total global citations (GCS), total local citations (LCS), h-index, g-index, m-index, GCS per document, LCS per document, year of first and last publication, and active years. Output is a sortable table and a horizontal bar chart of the top-N sources. Implemented by: Bibliometrix, SciMAT, HistCite.",
        category="Source / Journal Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="bradford_law",
        name="Bradford's Law",
        description="Apply Bradford's Law of Scattering to partition the journal list into three zones of decreasing productivity. Zone 1 (core): the small set of journals contributing one-third of all documents; zones 2 and 3 contain progressively more journals for each subsequent third. Output is a plot of cumulative document frequency vs journal rank on a log scale with zone boundaries marked, plus a table with columns: Source, Rank, Freq, cumFreq, Zone. Implemented by: Bibliometrix.",
        category="Source / Journal Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="source_over_time",
        name="Source Production Over Time",
        description="Line plot and table showing the yearly or cumulative number of documents published in each of the top-N most productive sources over the corpus timespan. The table has sources as columns and years as rows. Useful for tracking the rise and fall of specific journals in a field. Bibliometrix produces this as a dedicated source-over-time plot. ScientoPy can generate an equivalent time-series plot using sourceTitle as the analysis criterion. Note: the AGR, ADY, and PDLY metrics that ScientoPy computes alongside any criterion are separate features (see agr_metric, ady_metric, pdly_metric) and are not part of the production-over-time plot itself. Implemented by: Bibliometrix, ScientoPy.",
        category="Source / Journal Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="local_cited_sources",
        name="Most Local Cited Sources",
        description="Rank publication sources (journals, conference series) by how frequently they appear in the reference lists of the corpus documents (local citation score, LCS). Reveals the intellectual foundation sources of a research field: the journals whose papers are most read and cited by the community under study, independently of their global citation impact. Output is a bar chart and table sorted by local citation count. Implemented by: Bibliometrix.",
        category="Source / Journal Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Author Analysis ───────────────────────────────────────────────────────
    dict(
        id="author_metrics",
        name="Author Metrics (h, g, m-index)",
        description="Compute bibliometric impact indicators for each author in the corpus. Indicators: h-index (number h such that h papers have at least h citations each), g-index (largest g such that the top-g papers together have at least g^2 citations), m-index (h-index divided by years of active publication), total GCS, total LCS, OCC (document count), year of first and last publication. Output is a sortable table and a bar chart of top-N authors by selected indicator. CITAN additionally computes extended indices including the rp-index, lp-index, w-index, productivity, max citations, and sum of citations for ranked author assessment. Implemented by: Bibliometrix, SciMAT, HistCite, CITAN.",
        category="Author Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=False,
            CITAN=True,
        ),
    ),
    dict(
        id="author_profile",
        name="Author Profile (OpenAlex)",
        description="Retrieve and display a global author profile by querying the OpenAlex API for each author in the corpus. The global profile includes career-level metrics (total publications, total citations, h-index across all works, not only the local corpus), institutional affiliation history, and concept tags. Bibliometrix combines the global OpenAlex profile with a local profile computed from the loaded dataset. Implemented by: Bibliometrix.",
        category="Author Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="author_over_time",
        name="Author Production Over Time",
        description="Line plot and table showing the yearly or cumulative number of documents published by each of the top-N most productive authors over the corpus timespan. The table has authors as columns and years as rows, with document counts as values. Bibliometrix produces this as a dedicated author-over-time plot. ScientoPy can generate an equivalent time-series plot using author as the analysis criterion. Note: the AGR, ADY, and PDLY metrics that ScientoPy computes alongside any criterion are separate features (see agr_metric, ady_metric, pdly_metric) and are not part of the production-over-time plot itself. Implemented by: Bibliometrix, ScientoPy.",
        category="Author Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="lotka_law",
        name="Lotka's Law",
        description="Fit Lotka's inverse-square law to the empirical author productivity distribution and test goodness-of-fit. Lotka's Law states that the number of authors publishing n papers is proportional to 1/n^2. Output table contains: documents written, observed number of authors, observed proportion, and theoretical proportion under Lotka's Law. A Kolmogorov-Smirnov test statistic and p-value assess the fit quality. Implemented by: Bibliometrix.",
        category="Author Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Country & Affiliation Analysis ────────────────────────────────────────
    dict(
        id="country_production",
        name="Country Scientific Production",
        description="World choropleth map and bar chart showing the total number of documents attributed to each country over the entire corpus timespan. Country assignment uses the affiliation field of all authors (not only the first author). The map uses colour intensity proportional to document count. Bibliometrix produces the choropleth map. CiteSpace produces a similar geospatial overlay. Note: ScientoPy's time_line with country as criterion produces a production-over-time plot (see country_over_time), not a static total-count map. Implemented by: CiteSpace, Bibliometrix.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="country_mcp",
        name="Corresponding Author Country (SCP/MCP)",
        description="For each country, classify its documents as single-country publications (SCP: all authors from the same country) or multi-country publications (MCP: authors from two or more countries). Output table per country: total Articles, Articles %, SCP count, MCP count, MCP %. A high MCP ratio indicates a country that collaborates heavily with international partners. Analysis uses the corresponding-author country field. Implemented by: Bibliometrix.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="country_over_time",
        name="Country Production Over Time",
        description="Line plot showing the cumulative or yearly document counts for the top-N most productive countries over the corpus timespan. Each country is a separate line. The table has countries as columns and years as rows. Bibliometrix produces this as a dedicated country-over-time plot. ScientoPy can generate an equivalent time-series plot using country as the analysis criterion. Note: the AGR, ADY, and PDLY metrics that ScientoPy computes alongside any criterion are separate features (see agr_metric, ady_metric, pdly_metric) and are not part of the production-over-time plot itself. Implemented by: Bibliometrix, ScientoPy.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="affiliation_metrics",
        name="Affiliation / Institution Metrics",
        description="Rank institutions (universities, research centres, companies) by bibliometric indicators computed from the corpus. Indicators: document count (OCC), global citation score (GCS), local citation score (LCS), h-index, g-index. Output is a sortable table and a bar chart of top-N institutions. Note: ScientoPy can rank institutions by document count using institution as a criterion, but does not compute citation-based indicators (GCS, LCS, g-index) at institution level; that full metrics table is specific to Bibliometrix and CiteSpace. Implemented by: CiteSpace, Bibliometrix.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="affiliation_over_time",
        name="Affiliation Production Over Time",
        description="Line plot and table showing the cumulative or yearly number of documents per institution over the corpus timespan. The table has institutions as columns and years as rows. Useful for tracking the rise of specific research groups or centres as contributors to a field. Bibliometrix supports affiliation-over-time analysis via its R API. Implemented by: Bibliometrix.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="most_cited_countries",
        name="Most Cited Countries",
        description="Bar plot and table ranking countries by total global citations received by their documents in the corpus. Distinct from country production (which counts documents): this metric reveals which countries produce the most impactful work as measured by citation count. Computed using the country affiliation of all authors on each record. Implemented by: Bibliometrix.",
        category="Country & Affiliation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Keyword & Word Analysis ───────────────────────────────────────────────
    dict(
        id="keyword_frequency",
        name="Keyword Frequency & Ranking",
        description="Rank terms by occurrence count and citation impact across one or more controlled vocabularies. Bibliometrix supports: Author Keywords (DE field), Index Keywords (ID), combined Keywords, Title words, Abstract words, and WoS Subject Categories. Metrics per term: OCC, GCS, LCS, h-index, g-index, GCS/doc, LCS/doc, year of first and last occurrence. VOSviewer displays keywords only within co-occurrence networks, not as standalone ranked frequency tables. Implemented by: CiteSpace, Bibliometrix, SciMAT, CoPalRed, ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="wordcloud",
        name="Word Cloud",
        description="Generate a word cloud image in which the display size of each term is proportional to its occurrence frequency or citation count in the corpus. Bibliometrix and ScientoPy both expose word cloud as a dedicated graph type. Can be applied to any text field: author keywords, index keywords, titles, or abstracts. Implemented by: Bibliometrix, ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="treemap_words",
        name="Treemap of Words / Keywords",
        description="Display keyword or term proportions as a treemap chart in which each rectangle's area is proportional to its occurrence frequency. Provides a compact overview of the dominant topics in a corpus. Bibliometrix supports treemap visualisation of keyword and field frequencies. Implemented by: Bibliometrix.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="word_over_time",
        name="Word / Keyword Frequency Over Time",
        description="Line plot and table of cumulative or yearly occurrence counts per keyword over the corpus timespan. Each keyword is a separate line. Reveals when specific topics emerged, peaked, or declined in the literature. Bibliometrix, CiteSpace, and SciMAT produce this as a keyword frequency time series. ScientoPy can generate an equivalent time-series plot using any keyword criterion. Note: the AGR and PDLY metrics that ScientoPy computes alongside any criterion are separate features (see agr_metric, pdly_metric) and are not part of the frequency-over-time plot itself. Implemented by: CiteSpace, Bibliometrix, SciMAT, ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="trend_topics",
        name="Trend Topics",
        description="Identify trending and emerging keywords by computing growth statistics over a recent time window. Bibliometrix uses average growth rate (AGR) and the documents count in the last three years. CiteSpace uses burst-detection (Kleinberg's algorithm) to find keywords whose frequency increases sharply. SciMAT analyses keyword clusters by period. ScientoPy computes AGR and PDLY per topic and ranks them to identify the fastest-growing terms. Output: bar chart and table of top trending topics. Implemented by: CiteSpace, Bibliometrix, SciMAT, ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="noun_phrases",
        name="NLP Noun-Phrase Extraction",
        description="Extract multi-word noun phrases (NPs) from title and abstract text using NLP libraries (spaCy and/or TextBlob), and add them as additional concept fields alongside controlled-vocabulary keywords. NPs capture emerging terminology not yet indexed as author or index keywords. tm2+ is the only tool in this benchmark that implements this feature natively, producing NP-based frequency tables, word clouds, and co-occurrence networks using the same analysis classes as standard keyword fields. Implemented by: (none of the compared tools; unique tm2+ feature).",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="agr_metric",
        name="Average Growth Rate (AGR)",
        description="Compute the Average Growth Rate (AGR) for each topic (keyword, author, country, or any other criterion value) over a user-configurable recent time window (default: last 2 years). AGR = mean of year-over-year increases in document count over the window. A positive AGR indicates a growing topic; negative AGR indicates decline. Used by ScientoPy as the primary indicator for ranking trending topics and as the x-axis of the evolution plot. Implemented by: ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="ady_metric",
        name="Average Documents per Year (ADY)",
        description="Compute the Average Documents per Year (ADY) for each topic over a user-configurable recent time window. ADY = sum of documents in the window divided by number of years in the window. An absolute volume indicator: topics with high ADY are currently productive regardless of their growth rate. Used by ScientoPy alongside AGR and PDLY to give a three-dimensional picture of topic activity. Implemented by: ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="pdly_metric",
        name="Percentage of Documents in Last Years (PDLY)",
        description="Compute the Percentage of Documents in Last Years (PDLY) for each topic over a user-configurable recent time window. PDLY = ADY divided by total documents for that topic, times 100. A relative growth indicator showing what fraction of a topic's lifetime publications has appeared in the most recent period. High PDLY combined with high AGR identifies topics experiencing rapid recent growth. Used by ScientoPy as the y-axis of the evolution plot. Implemented by: ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="wildcard_search",
        name="Wildcard Topic Search (*)",
        description="Use an asterisk (*) wildcard character in topic search strings to match all values sharing a common prefix or suffix across any analysis criterion. Examples: 'smart*' matches 'smart city', 'smart home', 'smart grid', 'smart manufacturing'; '*learning' matches 'machine learning', 'deep learning', 'reinforcement learning'. All matching values are grouped under the wildcard pattern for frequency and trend analysis. Implemented by: ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="evolution_plot",
        name="Evolution Plot (Accumulative + AGR vs PDLY)",
        description="Two-panel evolution plot produced by ScientoPy. Left panel: accumulative document count per topic on a log-scale y-axis vs year, one line per topic, revealing long-term growth trajectories. Right panel: AGR (x-axis) vs PDLY (y-axis) parametric scatter, one point per topic, with quadrant lines at the median AGR and PDLY values dividing topics into four growth regimes (high absolute + high relative; high + low; low + high; low + low). Enables both historical and recent-growth comparison in one figure. Implemented by: ScientoPy.",
        category="Keyword & Word Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    # ── Document & Citation Analysis ──────────────────────────────────────────
    dict(
        id="cited_docs",
        name="Most Global / Local Cited Documents",
        description="Rank documents in the corpus by global citation count (GCS: total citations received worldwide according to the source database) and by local citation count (LCS: citations received from within the loaded corpus). Output is a bar chart and a table with columns: Document (author, year, title snippet), GCS, LCS, GCS/year. The most globally and most locally cited documents are often different, revealing both the field's landmark papers and its internal reference structure. Implemented by: CiteSpace, Bibliometrix, HistCite.",
        category="Document & Citation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="cited_references",
        name="Most Local Cited References",
        description="Rank individual cited references (strings in the reference lists of corpus documents) by the frequency with which they are cited within the corpus (local citation score). Unlike cited_docs, this operates on the raw reference strings and therefore captures foundational works that may not themselves be records in the corpus. Output is a table with columns: Reference string, Local citation count. Implemented by: CiteSpace, Bibliometrix, HistCite.",
        category="Document & Citation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="rpys",
        name="RPYS (Reference Publication Year Spectroscopy)",
        description="Reference Publication Year Spectroscopy (RPYS): plot the distribution of the publication years of all cited references in the corpus. Peaks in this distribution identify years in which foundational works appeared. A five-year median deviation curve highlights statistically significant peaks. Developed by Marx et al. (2014). Output is a line plot of citation age frequency vs year plus a table of peak years with the most-cited references from each peak. Implemented by: Bibliometrix.",
        category="Document & Citation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="hindex_topic",
        name="H-index per Topic / Criterion",
        description="Compute the h-index for any topic or criterion value (not only for individual authors). For a given keyword, country, journal, or institution, the h-index is the largest h such that h documents associated with that value have each been cited at least h times. Allows direct comparison of citation impact across topics and fields. Bibliometrix computes this for any bibliographic field; ScientoPy reports h-index per topic in its main frequency tables. Implemented by: Bibliometrix, SciMAT, HistCite, ScientoPy.",
        category="Document & Citation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=True,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    # ── Network Analysis ──────────────────────────────────────────────────────
    dict(
        id="coauthorship_net",
        name="Co-authorship Network",
        description="Construct and visualise a co-authorship network in which nodes are authors and edges connect pairs of authors who have co-authored at least one document in the corpus. Edge weight = number of co-authored documents. Node size = document count or citation count. Communities are detected by modularity clustering. Output includes: network visualisation, density map, degree-distribution table, and cluster membership lists. Implemented by: VOSviewer, CiteSpace, Bibliometrix, Gephi, SciMAT, CoPalRed.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=True,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="collaboration_net",
        name="Institution / Country Collaboration Network",
        description="Construct and visualise an institution-level or country-level collaboration network in which nodes are organisations or countries and edges represent co-authorship links. Edge weight = number of jointly authored documents. Reveals international and inter-institutional collaboration patterns. Output includes: network visualisation, community detection results, and a collaboration table. Implemented by: VOSviewer, CiteSpace, Bibliometrix, Gephi.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=True,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="country_worldmap",
        name="Country Collaboration World Map",
        description="Display country-to-country collaboration links as arcs on a world map, with arc thickness proportional to the number of jointly authored documents. Provides an immediate geographic overview of international collaboration patterns. Distinct from country_production (which shows document counts per country) and from collaboration_net (which shows the abstract network graph). Implemented by: Bibliometrix.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="cocitation_net",
        name="Co-citation Network",
        description="Construct and visualise a co-citation network in which nodes are cited references (or documents, or sources) and edges connect pairs cited together in the same documents. Clusters in the co-citation network represent schools of thought or sub-fields. Output: network visualisation, density map, cluster table, degree plot. CiteSpace and VOSviewer are the most commonly used tools for co-citation analysis. Implemented by: VOSviewer, CiteSpace, Bibliometrix, SciMAT, CoPalRed.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="cooccurrence_net",
        name="Keyword Co-occurrence Network",
        description="Construct and visualise a keyword co-occurrence network in which nodes are keywords (author keywords, index keywords, or both) and edges connect pairs appearing together in the same documents. Edge weight = number of co-occurrences. Community detection reveals thematic clusters. Output: network visualisation, diachronic animation, density map, node table, degree plot. Bibliometrix additionally supports co-occurrence for title words and abstract words. Implemented by: VOSviewer, CiteSpace, Bibliometrix, SciMAT, CoPalRed.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="coupling_net",
        name="Bibliographic Coupling Network",
        description="Construct and visualise a bibliographic coupling network in which nodes can be documents, authors, or sources, and edges connect pairs sharing at least one common reference. Edge weight = number of shared references. Bibliographic coupling clusters represent current research fronts. Bibliometrix supports coupling at document, author, and source levels with choice of coupling field (references, keywords, titles, abstracts). Output: network visualisation, centrality-impact diagram, cluster table. Implemented by: VOSviewer, Bibliometrix, SciMAT.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="diachronic_net",
        name="Diachronic / Animated Network",
        description="Produce an animated (diachronic) version of a network showing how nodes and edges appear and evolve over successive time windows. Each frame corresponds to a time slice (e.g. a 3-year window). CiteSpace is the canonical tool for diachronic network analysis with its timeline view and burst-detection overlay. Bibliometrix implements animated co-occurrence networks as part of its synthesis module. Implemented by: CiteSpace, Bibliometrix.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="network_density",
        name="Network Density Map",
        description="Overlay a kernel-density heat map on a network layout to show where nodes cluster most densely in the 2-D projection space. High-density regions indicate major research themes or author communities. VOSviewer is well known for its density visualisation mode, applicable to any network type (co-authorship, co-occurrence, co-citation). Bibliometrix provides an equivalent density map option. Implemented by: VOSviewer, Bibliometrix.",
        category="Network Analysis",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Thematic & Cluster Analysis ───────────────────────────────────────────
    dict(
        id="thematic_map",
        name="Thematic Map (Strategic Diagram)",
        description="Produce a strategic diagram (thematic map) that plots keyword clusters in a density-centrality space. The x-axis is centrality (strength of external links to other clusters) and the y-axis is density (strength of internal links within the cluster). The four quadrants classify themes as: motor themes (high centrality, high density), niche themes (low centrality, high density), basic/transversal themes (high centrality, low density), and emerging/declining themes (low centrality, low density). Output: strategic diagram, network of clusters, cluster assignment table, and documents per cluster. Implemented by: Bibliometrix, SciMAT.",
        category="Thematic & Cluster Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="thematic_evolution",
        name="Thematic Evolution",
        description="Track how research themes change across consecutive time periods by mapping cluster overlap between successive windows and drawing evolution arrows. A theme may split, merge, grow, or disappear over time. Bibliometrix implements thematic evolution as a Sankey-style flow diagram connecting the thematic maps of adjacent periods. SciMAT also implements longitudinal theme tracking across configurable time periods. Implemented by: Bibliometrix, SciMAT.",
        category="Thematic & Cluster Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    dict(
        id="factorial",
        name="Factorial Analysis (CA / MCA / MDS)",
        description="Apply factorial dimensionality-reduction methods to the term-document or term-term matrix to produce low-dimensional maps for visual interpretation. Bibliometrix implements: Correspondence Analysis (CA), Multiple Correspondence Analysis (MCA), and Multidimensional Scaling (MDS). These produce: word maps (terms in 2-D space), topic dendrograms (hierarchical clustering), words-by-cluster tables, and documents-by-cluster tables. SciMAT uses similar factorial methods in its science mapping pipeline. Implemented by: Bibliometrix, SciMAT.",
        category="Thematic & Cluster Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=True,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=False,
        ),
    ),
    # ── Reporting & Reproducibility ───────────────────────────────────────────
    dict(
        id="scripted_workflow",
        name="Scriptable / Reproducible Workflow",
        description="Expose all analysis functions through a scriptable API enabling fully reproducible and documented workflows. Bibliometrix provides a complete R package API and an RMarkdown report generator. ScientoPy is entirely CLI-driven: every analysis is a Python command with explicit parameters that can be saved in a shell script. CITAN provides a fully scriptable R API for all import, cleaning, and analysis operations. Implemented by: Bibliometrix, ScientoPy, CITAN.",
        category="Reporting & Reproducibility",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=True,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="gui",
        name="Graphical User Interface",
        description="Provide a graphical user interface allowing non-programmer users to drive the entire analysis workflow without writing code. Bibliometrix: Biblioshiny (R Shiny web app). VOSviewer: standalone Java desktop application. CiteSpace: Java desktop application. Gephi: standalone desktop application. SciMAT: Java desktop. CoPalRed: desktop application. HistCite: Windows desktop application. ScientoPy: ScientoPyUI front-end. Implemented by: VOSviewer, CiteSpace, Bibliometrix, Gephi, SciMAT, CoPalRed, HistCite, ScientoPy.",
        category="Reporting & Reproducibility",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=True,
            SciMAT=True,
            CoPalRed=True,
            HistCite=True,
            ScientoPy=True,
            CITAN=True,
        ),
    ),
    dict(
        id="export_plots",
        name="Export Plots (multiple formats)",
        description="Export generated figures in raster or vector formats for use in publications and presentations. Supported formats vary by tool: VOSviewer exports PNG and SVG; CiteSpace exports PNG and PDF; Bibliometrix (via R/ggplot2) exports PNG, SVG, PDF, EPS, and interactive HTML via plotly; Gephi exports PNG, SVG, PDF; SciMAT exports PNG; ScientoPy exports EPS, SVG, and PNG. Implemented by: VOSviewer, CiteSpace, Bibliometrix, Gephi, SciMAT, CoPalRed, ScientoPy.",
        category="Reporting & Reproducibility",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=True,
            SciMAT=True,
            CoPalRed=True,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="export_tabular",
        name="Tabular Export (TSV / CSV)",
        description="Export analysis results as structured tabular files (TSV, CSV, or Excel) for further processing in spreadsheet tools, statistical software, or custom scripts. ScientoPy exports per-topic tables including OCC per year, AGR, ADY, PDLY, and h-index as .tsv files. Bibliometrix exports results as CSV from Biblioshiny and as R data frames writable with write.csv(). Most tools (VOSviewer, CiteSpace, Gephi, SciMAT, CoPalRed, HistCite) also export network edge/node tables as CSV or text. Implemented by: VOSviewer, CiteSpace, Bibliometrix, Gephi, SciMAT, CoPalRed, HistCite, ScientoPy.",
        category="Reporting & Reproducibility",
        competitors=dict(
            VOSviewer=True,
            CiteSpace=True,
            Bibliometrix=True,
            Gephi=True,
            SciMAT=True,
            CoPalRed=True,
            HistCite=True,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    dict(
        id="previous_results",
        name="Chained / Filtered Sub-analysis",
        description="Use the filtered output document set from a previous query as the input corpus for a new analysis, enabling iterative drill-down without manual file editing. Example: first query retrieves all papers matching 'machine learning'; a second query uses that subset to find the top keywords within Canadian papers only. ScientoPy implements this via the --previous_results CLI flag, which reads the extended.tsv produced by the prior run as the new input dataset. Enables complex multi-step analytical pipelines. Implemented by: ScientoPy.",
        category="Reporting & Reproducibility",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=True,
            CITAN=False,
        ),
    ),
    # ── Bibliometric Storage & Data Management ────────────────────────────────
    dict(
        id="local_biblio_storage",
        name="Local Bibliometric Storage (Relational DB)",
        description="Persist imported bibliographic data in a local relational database (SQLite) rather than holding records only in memory or flat files. The database schema stores sources, documents, authors, languages, countries, and subject categories as normalised linked tables. This enables incremental imports across sessions (update of citation counts on re-import), cross-session querying, and the management of multiple analyses within a single database file without duplication. CITAN implements this as its core data model via an SQLite-backed local bibliometric storage (LBS). Implemented by: CITAN.",
        category="Bibliometric Storage & Data Management",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=True,
        ),
    ),
    dict(
        id="survey_grouping",
        name="Multi-Survey / Corpus Grouping",
        description="Organise imported documents into named, potentially overlapping groups (surveys) within a single database, allowing multiple bibliometric analyses to share the same underlying document pool without duplication. A document may belong to several surveys simultaneously. Analyses can be scoped to any survey by name. CITAN implements survey grouping as a first-class feature of its local bibliometric storage, enabling a single LBS file to serve multiple concurrent research questions. Implemented by: CITAN.",
        category="Bibliometric Storage & Data Management",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=True,
        ),
    ),
    dict(
        id="statistical_testing",
        name="Statistical Hypothesis Testing on Citation Data",
        description="Apply inferential statistical tests to citation count distributions to support evidence-based conclusions. Typical use: test whether review articles receive significantly more citations than regular articles using a non-parametric test (e.g. Wilcoxon rank-sum) appropriate for skewed citation distributions. Output includes the test statistic, p-value, and interpretation. CITAN integrates directly with R's statistical testing functions, enabling citation distributions extracted from the LBS to be passed to any R test. Implemented by: CITAN.",
        category="Document & Citation Analysis",
        competitors=dict(
            VOSviewer=False,
            CiteSpace=False,
            Bibliometrix=False,
            Gephi=False,
            SciMAT=False,
            CoPalRed=False,
            HistCite=False,
            ScientoPy=False,
            CITAN=True,
        ),
    ),
]

COMPETITORS = [
    "VOSviewer",
    "CiteSpace",
    "Bibliometrix",
    "Gephi",
    "SciMAT",
    "CoPalRed",
    "HistCite",
    "ScientoPy",
    "CITAN",
]
TM2_NAME = "tm2+"


# ═══════════════════════════════════════════════════════════════════════════════
#  SCORING
# ═══════════════════════════════════════════════════════════════════════════════


def compute_competitor_scores() -> dict[str, float]:
    total = len(FEATURES)
    counts = {n: 0 for n in COMPETITORS}
    for feat in FEATURES:
        for n in COMPETITORS:
            if feat["competitors"].get(n, False):
                counts[n] += 1
    return {n: round(counts[n] / total * 100, 1) for n in COMPETITORS}


def compute_tm2_score(impl: dict[str, bool]) -> float:
    total = len(FEATURES)
    count = sum(1 for f in FEATURES if impl.get(f["id"], False))
    return round(count / total * 100, 1)


def compute_coverage_scores(impl: dict[str, bool]) -> dict[str, float]:
    """
    For each competitor, score how well tm2+ covers that tool's own features.
    Score = features that BOTH the competitor AND tm2+ implement
            / features the competitor implements  x 100
    The competitor itself always scores 100 by definition.
    """
    scores = {}
    for name in COMPETITORS:
        comp_features = [f for f in FEATURES if f["competitors"].get(name, False)]
        total = len(comp_features)
        if total == 0:
            scores[name] = 0.0
            continue
        covered = sum(1 for f in comp_features if impl.get(f["id"], False))
        scores[name] = round(covered / total * 100, 1)
    return scores


# ═══════════════════════════════════════════════════════════════════════════════
#  YAML  (only for tm2+)
# ═══════════════════════════════════════════════════════════════════════════════


def load_tm2_yaml(path: str) -> dict[str, bool]:
    with open(path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    data = raw.get("features", raw)  # accept nested or flat
    return {str(k): bool(v) for k, v in data.items()}


def generate_template(dest: str = "tm2plus.yaml") -> None:
    lines = [
        "# tm2+ feature implementation status",
        "# Set each feature to true once implemented.",
        "features:",
    ]
    current_cat = None
    for feat in FEATURES:
        if feat["category"] != current_cat:
            current_cat = feat["category"]
            lines.append(f"\n  # {'─' * 4} {current_cat} {'─' * 4}")
        lines.append(f"  {feat['id']:<24}: false   # {feat['name']}")
    Path(dest).write_text("\n".join(lines) + "\n", encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════════
#  CONSOLE OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

BAR_WIDTH = 55
LABEL_WIDTH = 15


def _bar(score: float, char: str = "*") -> str:
    return char * round(score / 100 * BAR_WIDTH)


def print_chart(
    comp_scores: dict[str, float], tm2_score: float, tm2_impl: dict[str, bool]
) -> None:

    all_scores = {**comp_scores, TM2_NAME: tm2_score, "Gold Standard": 100.0}

    order = ["Gold Standard"] + [
        n
        for n, _ in sorted(
            ((k, v) for k, v in all_scores.items() if k != "Gold Standard"),
            key=lambda x: x[1],
            reverse=True,
        )
    ]

    for name in order:
        score = all_scores[name]
        is_gs = name == "Gold Standard"
        is_own = name == TM2_NAME
        char = "*"
        bar = _bar(score, char)
        print(f"  {name:<{LABEL_WIDTH-2}} |{bar:<{BAR_WIDTH}}|  {score:>5.1f}")


def print_coverage_chart(coverage_scores: dict[str, float]) -> None:
    """
    Second plot: each bar is a competitor tool (score = 100).
    The bar shows how much of that tool's feature set tm2+ already covers.
    """
    # Sort by tm2+ coverage descending
    sorted_items = sorted(coverage_scores.items(), key=lambda x: x[1], reverse=True)

    for name, score in sorted_items:
        comp_bar = _bar(100, "*")
        cover_bar = _bar(score, "*")
        gap = BAR_WIDTH - round(score / 100 * BAR_WIDTH)
        print(f"  {name:<{LABEL_WIDTH-2}} |{cover_bar}{'·' * gap}|  {score:>5.1f}")


def print_roadmap(tm2_impl: dict[str, bool]) -> None:
    pending = [f for f in FEATURES if not tm2_impl.get(f["id"], False)]
    W = LABEL_WIDTH + BAR_WIDTH + 14

    print()
    if not pending:
        print("  [Roadmap]  All features implemented — tm2+ matches the Gold Standard!")
        print()
        return

    print(f"  tm2+ ROADMAP  —  {len(pending)} features not yet implemented")
    print("-" * W)
    current_cat = None
    for feat in pending:
        if feat["category"] != current_cat:
            current_cat = feat["category"]
            print(f"\n  [ {current_cat} ]")
        print(f"    {feat['id']:<24}  {feat['name']}")
        print(f"    {'':24}  {feat['description']}")
    print()


def print_feature_table(tm2_impl: dict[str, bool]) -> None:
    all_sw = COMPETITORS + [TM2_NAME]
    col = 5
    id_w = 22
    W = id_w + 2 + len(all_sw) * col + 2

    print()
    print("  FULL FEATURE MATRIX")
    print("-" * W)
    # header
    hdr = "".join(f"{n[:col-1]:>{col}}" for n in all_sw)
    print(f"  {'Feature ID':<{id_w}}{hdr}")
    print("-" * W)

    current_cat = None
    for feat in FEATURES:
        if feat["category"] != current_cat:
            current_cat = feat["category"]
            cat_label = f"  {current_cat}"
            print(f"\n{cat_label}")
        cells = ""
        for name in COMPETITORS:
            v = feat["competitors"].get(name, False)
            cells += f"{'yes':>{col}}" if v else f"{'·':>{col}}"
        v_tm2 = tm2_impl.get(feat["id"], False)
        cells += f"{'YES':>{col}}" if v_tm2 else f"{'·':>{col}}"
        print(f"  {feat['id']:<{id_w}}{cells}")

    print()
    print("  Column order: " + "  ".join(all_sw))
    print("-" * W)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    yaml_path = args[0] if args else "tm2plus.yaml"

    if not Path(yaml_path).exists():
        print(f"[!]  YAML file not found: {yaml_path}")
        print(f"[+]  Generating template  →  tm2plus.yaml")
        generate_template("tm2plus.yaml")
        print("     Edit tm2plus.yaml (set features to true as you implement them)")
        print("     then re-run the script.")
        sys.exit(0)

    tm2_impl = load_tm2_yaml(yaml_path)
    comp_scores = compute_competitor_scores()
    tm2_score = compute_tm2_score(tm2_impl)
    coverage_scores = compute_coverage_scores(tm2_impl)

    print_chart(comp_scores, tm2_score, tm2_impl)
    print()
    print_coverage_chart(coverage_scores)
    if "--table" in flags:
        print_feature_table(tm2_impl)


if __name__ == "__main__":
    main()
