FEATURES: dict[str, set[str]] = {
    #
    # INGEST
    # ===================================================================================
    # data sources
    "import_wos": set("vp"),
    "import_scopus": set("vp"),
    "import_openalex": set("vp"),
    "import_pubmed": set(),
    "import_dimensions": set(),
    "import_lens": set(),
    "import_cochrane": set(),
    "merge_collections": set("vp"),
    #
    # item extraction
    "contains": set(),
    "country": set(),
    "difference": set(),
    "endswith": set(),
    "fullmatch": set(),
    "startswith": set(),
    "stemming_and": set(),
    "stemming_or": set(),
    "top_items": set(),
    #
    # column operations
    "coalesce_column": set(),
    "copy_column": set(),
    "count_column_items": set(),
    "exxtract_uppercase": set(),
    "ltwa_column": set(),
    "merge_columns": set(),
    "query": set(),
    "tokenize_column": set(),
    "transform_column": set(),
    "uppercase_column": set(),
    #
    # record review
    "coverage": set(),
    "find_records": set(),
    "filtered_records": set(),
    "record_viewer": set(),
    "record_mapping": set(),
    "statistics": set(),
    "summary_sheet": set(),
    #
    # ingestion review
    "extract_abstract_suffixes": set(),
    "extract_acronyms": set(),
    "extract_section_headers": set(),
    #
    # FILTERS
    # ===================================================================================
    "filter_doctype": set(),
    "filter_year": set(),
    "filter_citations": set(),
    "filter_field": set(),
    "filter_bradford": set(),
    "filter_language": set(),
    "filter_region": set(),
    "filter_subject": set(),
    #
    # REFINE/
    # ===================================================================================
    "concept_thesaurus": set(),
    "country_thesaurus": set(),
    "org_thesaurus": set(),
    "ref_thesaurus": set(),
    #
    # DISCOV/
    # ===================================================================================
    # Associations
    "lemma_butterfly_plot": set(),
    "lemma_metrics": set(),
    "lemma_associations": set(),
    "lemma_matrix_plot": set(),
    #
    # Co-occurrence matrix
    "co_occur_bubble_plot": set(),
    "co_occur_matrix_plot": set(),
    "co_occur_matrix": set(),
    "co_occur_matrix_list": set(),
    "co_occur_heatmap": set(),
    #
    # Concordance
    "kwic_concordance": set(),
    "record_term_report": set(),
    "record_term_search": set(),
    "sentence_concordance": set(),
    #
    # Auto-correlation
    "auto_correlation_matrix": set(),
    "auto_correlation_matrix_list": set(),
    "auto_correlation_heatmap": set(),
    "auto_correlation_map_plot": set(),
    #
    # Cross-correlation
    "cross_correlation_matrix": set(),
    "cross_correlation_matrix_list": set(),
    "cross_correlation_heatmap": set(),
    "cross_correlation_map_plot": set(),
    #
    # Cross-occurrence matrix
    "cross_occur_bubble_plot": set(),
    "cross_occur_heatmap": set(),
    "cross_occur_matrix_list": set(),
    "cross_occur_matrix_plot": set(),
    "cross_occur_matrix": set(),
    #
    # Document clustering
    "clusters_to_items_mapping": set(),
    "item_occurrences_by_cluster": set(),
    "items_by_cluter_dataframe": set(),
    "items_by_cluster_summary": set(),
    #
    # Life cycle
    "life_cycle_analysis": set(),
    #
    # Sankey three-field plot
    "sankey_three_field_plot": set(),
    #
    # TfIdf
    "tfidf_matrix": set(),
    #
    # ANALYZE
    # ===================================================================================
    # Annual metrics
    "annual_metrics": set(),
    "annual_metrics_plot": set(),
    #
    # Bradford's law
    "bradford_law_plot": set(),
    "bradford_law_zones": set(),
    "bradford_law_table": set(),
    #
    # Lotka's law
    "lotka_law_plot": set(),
    "lotka_law_table": set(),
    #
    # Item Occurrence
    "occurrence_bar_plot": set(),
    "occurrence_dot_plot": set(),
    "occurrence_column_plot": set(),
    "occurrence_line_plot": set(),
    "occurrence_metrics": set(),
    "occurrence_pie_plot": set(),
    "occurrence_ranking_plot": set(),
    "occurrence_wordcloud": set(),
    "occurrence_worldmap": set(),
    #
    # RPYS
    "rpys_plot": set(),
    "rpys_table": set(),
    #
    # Trend topics
    "bibliometrix_trend_topics": set(),
    "bursts": set(),
    "scientopy_trend_topics": set(),
    #
    # Trends
    "cumulative_trends_plot": set(),
    "cumulative_trends": set(),
    "gantt_plot": set(),
    "trends": set(),
    #
    # Zipf's law
    "zipf_law_plot": set(),
    "zipf_law_table": set(),
    #
    # SYNTHESIZE
    # ===================================================================================
    # collaboration
    "collaboration_bar_plot": set(),
    "collaboration_metrics": set(),
    "collaboration_worldmap": set(),
    #
    # Emergence
    "emergence_items_table": set(),
    "emergence_items_plot": set(),
    #
    # Main path
    "main_path_documents": set(),
    "main_path_plot": set(),
    "main_path_edges": set(),
    #
    # Topic modeling
    "cluster_to_items_mapping": set(),
    "components_to_item_dataframe": set(),
    "documents_by_theme_dataframe": set(),
    "items_by_theme_dataframe": set(),
    "theme_to_documents_mapping": set(),
    #
    #
}
