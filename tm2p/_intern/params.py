from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd  # type: ignore
from sklearn.base import BaseEstimator  # type: ignore

from tm2p.enum import (
    AssociationIndex,
    CitationUnit,
    CoCitationUnit,
    Correlation,
    CouplingUnit,
    Field,
    ItemOrderBy,
    RecordOrderBy,
)


@dataclass
class Params:

    #
    # Ingestion and basic operations:
    #
    source_field: Field
    source_fields: tuple[Field, ...]
    target_field: Field
    stemming_fn: Callable

    #
    # Occurrence matrix:
    #
    column_field: Field
    index_field: Field

    #
    # Cross-correlation operations:
    #
    cross_field: Field

    #
    # Ingestion and basic operations:
    #
    item_citations_range: Tuple[Optional[int], Optional[int]] = (None, None)
    item_occurrences_range: Tuple[Optional[int], Optional[int]] = (None, None)
    items_in: Optional[list[str]] = None
    items_order_by: ItemOrderBy = ItemOrderBy.OCC
    top_n: Optional[int] = None

    #
    # Occurrence matrix:
    #
    column_item_citations_range: Tuple[Optional[int], Optional[int]] = (None, None)
    column_item_occurrences_range: Tuple[Optional[int], Optional[int]] = (None, None)
    column_items_in: Optional[list[str]] = None
    column_items_order_by: ItemOrderBy = ItemOrderBy.OCC
    column_top_n: Optional[int] = None

    index_item_citations_range: Tuple[Optional[int], Optional[int]] = (None, None)
    index_item_occurrences_range: Tuple[Optional[int], Optional[int]] = (None, None)
    index_items_in: Optional[list[str]] = None
    index_items_order_by: ItemOrderBy = ItemOrderBy.OCC
    index_top_n: Optional[int] = None

    #
    # Citation network:
    #
    citation_unit: CitationUnit = CitationUnit.AUTH

    #
    # Co-citation network:
    #
    co_citation_unit: CoCitationUnit = CoCitationUnit.CITED_AUTH

    #
    # Coupling network:
    #
    coupling_unit: CouplingUnit = CouplingUnit.AUTH

    #
    # Plotting:
    #
    plotting_column = None

    #
    # A
    #
    association_index: AssociationIndex = AssociationIndex.NONE
    axes_visible: bool = False

    #
    # B
    #
    baseline_periods: int = 3
    binary_item_frequencies: bool = False

    #
    # C
    #
    case_sensitive: bool = False
    citation_threshold: int = 0
    cluster_coverages: Optional[list[str]] = None
    cluster_names: Optional[list[str]] = None
    clustering_algorithm_or_dict: Optional[Union[str, dict]] = None
    color: Optional[str] = None
    colored_output: bool = True
    colored_stderr: bool = True
    colormap: str = "Blues"
    column: Optional[str] = None
    contour_opacity: float = 0.6
    core_area: Optional[str] = None
    correlation_method: Correlation = Correlation.PEARSON
    cumulative_sum: bool = False
    similarity_cutoff: float = 85.0

    #
    # D
    #
    decomposition_algorithm: Optional[BaseEstimator] = None
    draw_arrows: bool = False

    #
    # E
    #
    edge_colors: Tuple[Any, ...] = ("#b8c6d0",)
    edge_opacity_range: Tuple[float, float] = (0.1, 0.9)
    edge_similarity_threshold: float = 0.0
    edge_top_n: Optional[int] = None
    edge_width_range: Tuple[float, float] = (0.5, 0.8)
    edge_widths: Tuple[
        Union[float, int],
        Union[float, int],
        Union[float, int],
        Union[float, int],
    ] = (0.5, 0.8, 1.0, 1.2)

    #
    # I
    #
    initial_newline: bool = False
    counters: bool = True
    items_per_year: int = 5

    #
    # K
    #
    kernel_bandwidth: float = 0.1
    keys_order_by: str = "alphabetical"
    kleinberg_burst_rate: float = 2.0
    kleinberg_burst_gamma: float = 1.0

    #
    # L
    #
    line_color: Union[str, float, Sequence[float]] = "black"
    line_width: float = 1.5

    #
    # M
    #
    manifold_algorithm: Optional[BaseEstimator] = None
    marker_size: float = 7
    fuzzy_threshold: float = 95.0
    maximum_occurrence: int = 10
    minimum_items_in_cluster: int = 5
    minimum_number_of_clusters: int = 10

    #
    # N
    #
    n_chars: int = 100
    n_contexts: int = 10
    node_colors: tuple[Union[str, float, Sequence[float]], ...] = ("#7793a5", "#465c6b")
    node_size_range: Tuple[int, int] = (5, 20)
    node_size: int = 10
    node_n_labels: int = 1000
    novelty_threshold: float = 0.15

    #
    # O
    #
    occurrence_threshold: int = 2

    #
    # P
    #
    pattern: Union[str, tuple[str, ...]] = ""
    periods_with_at_least_one_record: int = 3
    pie_hole: float = 0.4
    plot_dimensions: Tuple[int, int] = (0, 1)
    plot_height: float = 400
    plot_width: float = 400
    preferred_key: str = ""

    #
    # Q
    #
    query_expression: Optional[str] = None
    quiet: bool = False

    #
    # R
    #
    ratio_threshold: float = 0.5
    recent_periods: int = 3
    record_citations_range: Tuple[Optional[int], Optional[int]] = (None, None)
    record_years_range: Tuple[Optional[int], Optional[int]] = (None, None)
    records_match: Optional[Dict[Field, List[str]]] = None
    records_order_by: RecordOrderBy = RecordOrderBy.YEAR_NEWEST
    regex_flags: int = 0
    regex_search: bool = False
    replacement: Optional[str] = None
    root_directory: str = "./"

    #
    # S
    #
    spring_layout_iterations: int = 50
    spring_layout_k: Optional[float] = 0.1
    spring_layout_seed: int = 42

    #
    # T
    #
    textfont_color: Union[str, float, Sequence[float]] = "#465c6b"
    textfont_opacity_range: Tuple[float, float] = (0.5, 1)
    textfont_opacity: float = 1.0
    textfont_size_range: Tuple[float, float] = (8.0, 16.0)
    textfont_size: float = 10
    tfidf_norm: Optional[str] = None
    tfidf_smooth_idf: bool = False
    tfidf_sublinear_tf: bool = False  # sublinear_tf
    tfidf_use_idf: bool = False  # using_idf_reweighting
    thesaurus_file: str = "no_name.the.txt"
    time_window: int = 2
    title_text: Optional[str] = None
    top_items_by_theme: int = 5
    total_records_threshold: int = 7
    tqdm_disable: bool = False
    transformation_function: Optional[Callable[[pd.Series], pd.Series]] = None

    #
    # U
    #
    unit_of_analysis: Optional[str] = None

    #
    # V
    #
    variant_keys: tuple[str, ...] = ()

    #
    # X
    #
    xaxes_range: Optional[Tuple[float, float]] = None
    xaxes_title_text: Optional[str] = None

    #
    # Y
    #
    yaxes_range: Optional[Tuple[float, float]] = None
    yaxes_title_text: Optional[str] = None
    yshift: float = 4

    #
    # W
    #
    word: Optional[str] = None
    word_length: int = 50

    #
    # Z
    #
    zotero_api_key: Optional[str] = None
    zotero_library_id: Optional[str] = None
    zotero_library_type: Optional[str] = None

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__annotations__:
                raise ValueError(f"Unknown parameter: {key}")
            setattr(self, key, value)
        return self
