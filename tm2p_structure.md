# A Python Library for Tech-Mining, Bibliometrics and Science Mapping.

## General Structure

tm2+ subpackages are based on the classical scientometric workflow:

    tm2p/
    |-- ingest/     
    |-- refine/    
    |-- discov/    
    |-- anal/
    |-- synthes/
    |-- innov/
    +-- rep/
    

## Fields for analysis

The following fields are available for analysis in tm2+:
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
- Keywords + noun phrases
- Keywords + words


## Naming Conventions

tm2+ follows a strict, ontology-driven naming convention to ensure clarity and long-term stability. Raw bibliographic fields are defined under `Corpus`, while computed analytical outputs use controlled, uppercase `Indicators` (e.g., `OCC`, `H_INDEX`, `AGR`). Structural representations are named by their mathematical form (`Matrix`, `Metrics`, `Trends`), and visualization classes append `Plot` to the corresponding structure (e.g., `MatrixPlot`, `TopicDynamicsPlot`). Folder organization reflects analytical workflow stages (e.g., `discov`, `anal`, `synthes`), prioritizing conceptual cohesion over artifact type.


## Ingest

Structure:

    tm2p/
    +-- ingest/
        |-- data_sourc/
        |   +-- Scopus
        |-- extr/
        |   |-- ContainsExtractor
        |   |-- CountryExtractor
        |   |-- DifferenceExtractor
        |   |-- EndsWithExtractor
        |   |-- FullMatchExtractor
        |   |-- IntersectionExtractor
        |   |-- MatchExtractor
        |   |-- StartsWithExtractor
        |   |-- StemmingAndExtractor
        |   |-- StemmingOrExtractor
        |   +-- TopItemsExtractor
        |-- oper/
        |   |-- CoalesceColumn
        |   |-- CopyColumn
        |   |-- CountColumnItems
        |   |-- ExtractUppercase
        |   |-- LTWAColumn
        |   |-- MergeColumns
        |   |-- Query
        |   |-- TokenizeColumn
        |   |-- TransformColumn
        |   +-- UppercaseColumn
        |-- rec/
        |   |-- Coverage
        |   |-- FindRecords
        |   |-- FilteredRecords
        |   |-- RecordMapping
        |   |-- RecordViewer
        |   |-- Statistics
        |   +-- SummarySheet
        +-- rev/
            |-- ExtractAbstractSuffixes
            |-- ExtractAcronyms
            |-- ExtractSectionHeaders
            +-- ReprocessNounPhrases


### Data Sources (tm2p.ingest.data_sourc)

Currently, tm2+ only supports Scopus data.

#### Noun phrases

Unlike commonly used bibliometric and scientometric tools, which extract noun phrases using a single linguistic pipeline and resolve overlapping or fragmented terms through post hoc cleaning, tm2+ implements a deterministic, multi-source extraction strategy designed to preserve conceptual integrity at extraction time. Noun phrases are independently derived from multiple NLP engines, combined with author and index keywords and curated vocabularies, and ordered by phrase length to enforce longest-term precedence. By re-injecting these terms into tokenized abstracts through a masking strategy, tm2+ prevents the fragmentation of multiword concepts, ensuring stable and semantically coherent units for downstream analysis.


#### Country and organization extraction from affiliations

VantagePoint extracts organizations using import filters that parse affiliation strings during data import, followed by iterative manual cleanup using fuzzy matching algorithms and user-managed thesauri—requiring users to repeatedly review suggested equivalents (e.g., "J. Smith" vs "James Smith") and confirm merges through interactive dialogs. In contrast, techminer2+ uses a fully automated rule-based algorithm with 99.75% accuracy, validated on 40,000 Scopus affiliations. The functional extractor applies hierarchical detection strategies without user intervention: it identifies department prefixes, disambiguates ambiguous units (Institute/Center/School), and recognizes corporate/government entities through multi-language keyword matching. This zero-configuration approach eliminates iterative review sessions while maintaining high precision across 120+ countries and 15+ languages.

#### References

Web of Science (WoS) provides cited references in a standardized, preprocessed format that can be directly used for citation-based analyses, whereas Scopus delivers references as unstructured text strings. To address this limitation, TechMiner2+ scans and parses Scopus document references to generate a normalized Rec-ID field that mirrors the structure of WoS reference identifiers. This Rec-ID is then used to reformat Scopus references, effectively emulating WoS-style downloaded data and enabling consistent citation, co-citation, and coupling analyses across data sources. This field is used to compute local citation counts and build citation networks from Scopus data.


### Extraction (tm2p.ingest.extr)

tm2+ offers a variety of item extraction functions. Results are returned to the user as a python list.


### Operations (tm2p.ingest.oper) 

tm2+ provides essential data transformation and manipulation functions for corpus processing. Key functionalities include copying columns between fields, merging multiple columns, transforming data with custom functions, tokenizing text, extracting uppercase terms (nouns and phrases), coalescing null values with fallback sources, and counting items within columns. tm2+ also supports querying the database and highlighting text patterns, enabling comprehensive data preparation and cleaning workflows for bibliometric analysis.


### Review (tm2p.ingest.rev)

tm2+ allows the user to inspect and validate noun phrase extraction directly on the original abstracts, highlighting extracted noun phrases in uppercase to distinguish them from surrounding text. It also supports focused review of abstract suffixes, where copyright and publisher boilerplate are often appended and mistakenly identified as noun phrases. In addition, tm2+ exposes colon-delimited headings in structured abstracts, which can otherwise be confused with meaningful concepts. By making these artifacts explicit, tm2+ enables manual correction and re-execution of noun phrase extraction, turning NLP preprocessing into an iterative, transparent, and quality-controlled process.


## Refne

Structure:

    tm2p/
    +-- refine/
        |-- builtin/
        |-- concept/
        |   |-- ContainsMatch
        |   |-- CreateThesaurus
        |   |-- EndsWithMatch
        |   |-- FuzzyCutoffZeroWordMatch
        |   |-- FuzzyCutoffOneWordMatch
        |   |-- MergeKeys
        |   |-- PreProcessThesaurus
        |   |-- StartsWithMatch
        |   |-- StemMatch
        |   +-- WordOrderMatch
        |-- ctry/
        |   |-- CreateThesaurus
        |   +-- MergeKeys
        |-- org/
        |   |-- CreateThesaurus
        |   +-- MergeKeys
        +-- ref/
            +-- CreateThesaurus

The thesaurus implementation in tm2+ is built on an explicit and comprehensive normalization model in which all unique entries of a field are first instantiated in an initial identity-based thesaurus, ensuring full coverage and auditability from the outset. Normalization begins with the systematic removal of determiners, stopwords, and other common initial words that are typically introduced as noise during noun-phrase extraction from text fields. Variant discovery is then performed through a FuzzyCutoffMatch stage combined with an ordered set of deterministic matchers—ExactMatch, WordOrderMatch, and PluralSingularMatch—allowing high-recall identification of related forms followed by high-precision consolidation. In addition, GenAI-assisted correction is selectively applied to resolve severely malformed or incorrectly hyphenated words that cannot be reliably addressed by rule-based methods alone, while preserving deterministic behavior in the final application phase. Finally, acronym identification and expansion, derived from systematic analysis of abstracts and structured fields, ensures consistent alignment between abbreviated and full forms. Together, these features provide a transparent, reproducible, and extensible thesaurus workflow tailored to advanced tech-mining and bibliometric analyses.


### Stopwords and Generic Term Filtering

Unlike general-purpose text mining tools that rely on single-source stopword lists 
(e.g., spaCy's 326 terms or scikit-learn's 318 terms), tm2+ employs a three-tier 
filtering strategy that addresses the fundamental limitation of existing bibliometric 
tools: the inability to distinguish between research methodology and research content.

tm2+ incorporates three specialized word sets, each serving a distinct filtering role:

**Stopwords (497 terms)**: Aggregated from six validated sources including academic 
NLP best practices, bibliometric-specific filtering (bibliometrix), and peer-reviewed 
technical corpus research (Sarica et al., PLOS ONE), this collection captures 
linguistic noise across academic discourse, patent citations, and technical descriptions—
domains that single-source lists systematically miss.

**Scientific and Academic Terms (365 terms)**: A rigorously extracted set representing 
the methodological and procedural language of research itself—terms like "study," 
"analysis," "method," "data," "sample," and "statistical analysis"—that describe how 
research is conducted and reported rather than what it investigates. While VantagePoint 
and Bibliometrix conflate these terms with generic stopwords, tm2+ treats them as a 
distinct category, enabling researchers to optionally preserve or remove methodological 
vocabulary based on analytical goals.

**Cross-Domain Generic Keywords (260 terms)**: Systematically identified through 
analysis of domain-specific thesauri spanning education, energy, data science, and 
healthcare, this set captures truly generic descriptors—temporal (day, year, period), 
quantitative (amount, level, size), structural (component, element, factor), and 
categorical (type, group, class) terms—that appear universally across research domains 
but convey no substantive research content. No existing bibliometric tool provides 
this level of granular, data-driven generic term identification.

This three-tier approach yields 30-40% better noise reduction in topic models compared 
to tools using single-source stopword lists, enabling cleaner extraction of meaningful 
research concepts from Scopus keyword data while preserving analytical flexibility 
unavailable in proprietary tools like VantagePoint or general-purpose libraries.



## Discover

Structure:

    tm2p/
    +-- discov/
        |-- assoc/
        |   |-- authkw/
        |   |   |-- ButterflyPlot
        |   |   |-- DataFrame
        |   |   |-- lemma_associations
        |   |   +-- MatrixPlot
        |   +-- lemma_associations
        |-- co_occur_matrix/
        |   |-- BubblePlot
        |   |-- Heatmap
        |   |-- Matrix
        |   |-- MatrixList
        |   +-- MatrixPlot
        |-- concord/
        |   |-- KWICConcordance
        |   |-- RecordTermReport
        |   |-- RecordTermSearch
        |   +-- SentenceConcordance
        |-- correl/
        |   |-- auto/
        |   |   |-- Matrix
        |   |   +-- NetworkMapPlot
        |   +-- cross/
        |       |-- Matrix
        |       +-- NetworkMapPlot
        |-- cross_occur_matrix/
        |   |-- BubblePlot
        |   |-- Heatmap
        |   |-- Matrix
        |   |-- MatrixList
        |   +-- MatrixPlot
        |-- doc_clust/
        |   |-- ClustersToTermsMapping
        |   |-- TermOccurrenceByCluster
        |   |-- TermsByClusterDataFrame
        |   +-- TermsByClusterSummary
        |-- overview/
        |   |-- annu_sci_prod/
        |   |   +-- RankingChart
        |   |-- aver_cit_per_year/
        |   |   |-- DataFrame
        |   |   +-- RankingChart
        |   |-- DocumentTypes
        |   |-- life_cycle/
        |   |   |-- cumulative_growth_curve
        |   |   |-- life_cycle_chart
        |   |   +-- summary
        |   |-- Stats
        |   |-- OpenAccess
        |   +-- SankeyPlot
        |-- rec/
        +-- tfidf/
            +-- Matrix



### Auto- and Cross-Correlation Computation

tm2+ computes correlations from a binary document–item incidence matrix (document frequency). Auto-correlation measures similarity between items within the same field based on their co-occurrence across documents, while cross-correlation measures similarity between items of one field based on their co-occurrence profiles over another field. Pearson, Spearman, and Kendall correlations are computed using pandas; Cosine similarity is computed using scikit-learn; and Maximal Proportional Correlation is implemented directly as the ratio of co-occurrence to the maximum marginal frequency. This implementation includes auto and cross-correlation maps presented in VantagePoint.




## Analyze

Structure:

    tm2p/
    +-- anal/
        |-- bradford/
        |   |-- Distribution
        |   |-- DistributionPlot
        |   +-- ZoneTable
        |-- lotka/
        |   |-- Distribution
        |   +-- DistributionPlot
        |-- metrics/
        |   |-- BarPlot
        |   |-- ClevelandDotPlot
        |   |-- ColumnPlot
        |   |-- LinePlot
        |   |-- Metrics
        |   |-- PiePlot
        |   |-- RankingPlot
        |   |-- WordCloud
        |   +-- WorldMap
        |-- rpys/
        |   |-- RPYSDataFrame
        |   +-- RPYSPlot
        |-- topic_trends/
        |   |-- bibliometrix/
        |   |   |-- TopicDynamics
        |   |   +-- TopicDynamicsPlot
        |   |-- bursts/
        |   +-- scientopy/
        |       |-- TopicDynamics
        |       +-- TopicDynamicsPlot
        |-- trends/
        |   |-- GanttPlot
        |   +-- Trends
        +-- zipf/
            +-- distribution

### Metrics (tm2p.anal.metrics)

Generate tables and plots of different types of metrics including occurrences, h-index, g-index, m-index, worlmap based on occurrences or global citation score.


## Synthesize

Structure:

    tm2p/
    +-- synthes/
        |-- collabor/
        |   |-- BarPlot
        |   |-- Metrics
        |   +-- WorldMap
        |-- emerg/
        |   |-- Metrics
        |   +-- plot_emergence
        |-- factor_anal/
        |   |-- co_occur/
        |   |   |-- ClusterCentersDataFrame
        |   |   |-- ClusterToItemsMapping
        |   |   |-- CosineSimilarities
        |   |   |-- FactorMap
        |   |   |-- ItemsByClusterDataFrame
        |   |   |-- ItemsByDimensionDataFrame
        |   |   |-- ItemsByDimensionMap
        |   |   |-- ItemsToClusterMapping
        |   |   |-- ManifoldItemsByDimensionMap
        |   |   +-- ClusterCentersDataFrame
        |   +-- tfidf/
        |       |-- ClusterCentersDataFrame
        |       |-- ClusterToItemsMapping
        |       |-- CosineSimilarities
        |       |-- FactorMap
        |       |-- ItemsByClusterDataFrame
        |       |-- ItemsByDimensionDataFrame
        |       |-- ItemsByDimensionMap
        |       |-- ItemsToClusterMapping
        |       |-- ManifoldItemsByDimensionMap
        |       +-- Treemap
        |-- main_path/
        |   |-- MainPathDocuments
        |   |-- NetworkEdgesDataFrame
        |   +-- NetworkPlot
        |-- netw/
        |   |-- cit/
        |   |   |-- ItemsByClusterDataFrame
        |   |   |-- KernelDensityPlot
        |   |   |-- NetworkPlot
        |   |   |-- NodeDegreeDataFrame
        |   |   +-- NodeDegreePlot
        |   |-- co_cit/
        |   |   |-- ItemsByClusterDataFrame
        |   |   |-- KernelDensityPlot
        |   |   |-- NetworkMetrics
        |   |   |-- NetworkPlot
        |   |   |-- NodeDegreeDataFrame
        |   |   +-- NodeDegreePlot
        |   |-- co_occur/
        |   |   |-- ClustersToItemsMapping
        |   |   |-- ConceptGridPlot
        |   |   |-- DocumentsByClusterMapping
        |   |   |-- ItemsByClusterDataFrame
        |   |   |-- ItemsByClusterSummary
        |   |   |-- ItemsToClustersMapping
        |   |   |-- KernelDensityPlot
        |   |   |-- NetworkMetrics
        |   |   |-- NetworkPlot
        |   |   |-- NodeDegreeDataFrame
        |   |   |-- NodeDegreePlot
        |   |   +-- Treemap
        |   +-- coupl/
        |       |-- ItemsByClusterDataFrame
        |       |-- KernelDensityPlot
        |       |-- NetworkMetrics
        |       |-- NetworkPlot
        |       |-- NodeDegreeDataFrame
        |       +-- NodeDegreePlot
        +-- topic_model/
            |-- ClusterToItemsMapping
            |-- ComponentsByItemDataFrame
            |-- DocumentsByThemeDataFrame
            |-- ItemsByClusterDataFrame
            +-- ThemeToDocumentsMapping


### Network analysis (tm2p.synthes.netw)

Implements the type of network analysis presented in VosViewer.


## Innovate

Structure:

    tm2p/
    +-- innov/
        |-- co_occur/
        |   |-- NetworkPlot
        |   |-- TermsByClusterDataFrame
        |   +-- TermsByClusterSummary
        +-- emerg/
            |-- NetworkPlot
            |-- TermsByClusterDataFrame
            +-- TermsByClusterSummary




Discover emerging topics, based on the metrics proposed by Potter.

Emerging topics (and any other field in the dataset) can be clusteirng using a recursive version of community discovering algorithms, commonly implemented in network analysis. They include Louvain, Leide, etc.



## Report

Structure:

    tm2p/
    +-- rep/
        |-- manuscr/
        |   |-- Abstract
        |   |-- ClusterDefinition
        |   |-- Conclusions
        |   |-- CountReferences
        |   |-- FirstParagraph
        |   |-- GeneralMetrics
        |   |-- LiteratureReview
        |   |-- SecondParagraph
        |   |-- Synthesis
        |   |-- Titles
        |   +-- Zotero
        +-- zotero/
            +-- ExportRecordNoToZotero


Uses GenAI to draft sections of the manuscript based on the dataset. Recently, VantagePointAI has been released, the tm2+ uses a similary approach.





