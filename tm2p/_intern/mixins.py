from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union, cast

import pandas as pd  # type: ignore
from sklearn.base import BaseEstimator  # type: ignore
from typing_extensions import Self

from tm2p._intern.valid import (
    check_optional_base_estimator,
    check_optional_positive_float,
    check_optional_positive_int,
    check_optional_str,
    check_optional_str_list,
    check_optional_str_or_dict,
    check_plotly_color,
    check_required_bool,
    check_required_color_list,
    check_required_corpus_field_enum,
    check_required_float,
    check_required_float_0_1,
    check_required_float_0_1_range,
    check_required_float_range,
    check_required_int,
    check_required_int_range,
    check_required_items_order_by_enum,
    check_required_non_negative_float,
    check_required_non_negative_int,
    check_required_open_ended_int_range,
    check_required_positive_float,
    check_required_positive_float_range,
    check_required_positive_int,
    check_required_positive_number_range,
    check_required_str,
    check_required_str_or_str_tuple,
    check_required_str_tuple,
    check_tuple_of_ordered_four_floats,
)
from tm2p.enum import (
    AssociationIndex,
    CitationUnit,
    Correlation,
    CouplingUnit,
    Field,
    ItemOrderBy,
    RecordOrderBy,
)
from tm2p.enum.co_cit_unit import CoCitationUnit

from .params import Params


class SortAxesMixin:

    def sort_columns(self, data_frame):
        counters = pd.DataFrame({"term": data_frame.columns.tolist()})
        counters = self._extract_term_occurrences(counters)
        counters = self._extract_citation_counts(counters)
        sorted_topics = self._rank_terms_by_count_and_citations(counters)
        data_frame = data_frame[sorted_topics]
        return data_frame

    def sort_index(self, data_frame):
        counters = pd.DataFrame({"term": data_frame.index.tolist()})
        counters = self._extract_term_occurrences(counters)
        counters = self._extract_citation_counts(counters)
        sorted_topics = self._rank_terms_by_count_and_citations(counters)
        data_frame = data_frame.loc[sorted_topics, :]
        return data_frame

    def _rank_terms_by_count_and_citations(self, counters):
        counters = counters.sort_values(
            by=["OCC", "citations", "term"], ascending=[False, False, True]
        )
        sorted_topics = counters.term.tolist()
        return sorted_topics

    def _extract_citation_counts(self, counters):
        counters["citations"] = counters.term.str.split()
        counters["citations"] = counters["citations"].map(lambda x: x[-1])
        counters["citations"] = counters["citations"].str.split(":")
        counters["citations"] = counters["citations"].map(lambda x: x[1]).astype(int)
        return counters

    def _extract_term_occurrences(self, counters):
        counters["OCC"] = counters.term.str.split()
        counters["OCC"] = counters["OCC"].map(lambda x: x[-1])
        counters["OCC"] = counters["OCC"].str.split(":")
        counters["OCC"] = counters["OCC"].map(lambda x: x[0]).astype(int)
        return counters


class ParamsMixin:

    def __init__(self, **kwargs):
        self.params = Params()
        self.update(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.params, key, value)
        return self

    # ==========================================================================
    # HAVING_* → Item filtering (WHICH items?)
    # ==========================================================================

    def having_case_sensitive(self, case_sensitive: bool) -> Self:
        case_sensitive = check_required_bool(
            value=case_sensitive,
            param_name="case_sensitive",
        )
        self.params.case_sensitive = case_sensitive
        return self

    def having_column_item_citations_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "column_item_citations_range"
        )
        self.params.column_item_citations_range = (start, end)
        return self

    def having_column_item_occurrences_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "column_item_occurrences_range"
        )
        self.params.column_item_occurrences_range = (start, end)
        return self

    def having_column_items_in(self, column_items_in: Optional[list[str]]) -> Self:
        column_items_in = check_optional_str_list(
            value=column_items_in,
            param_name="column_items_in",
        )
        self.params.column_items_in = column_items_in
        return self

    def having_column_items_in_top(self, column_top_n: Optional[int]) -> Self:
        column_top_n = check_optional_positive_int(
            value=column_top_n,
            param_name="column_top_n",
        )
        self.params.column_top_n = column_top_n
        return self

    def having_column_items_ordered_by(
        self, column_items_order_by: ItemOrderBy
    ) -> Self:
        column_items_order_by = check_required_items_order_by_enum(
            value=column_items_order_by,
            param_name="column_items_order_by",
        )
        self.params.column_items_order_by = column_items_order_by
        return self

    def having_index_item_citations_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "index_item_citations_range"
        )
        self.params.index_item_citations_range = (start, end)
        return self

    def having_index_item_occurrences_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "index_item_occurrences_range"
        )
        self.params.index_item_occurrences_range = (start, end)
        return self

    def having_index_items_in(self, index_items_in: Optional[list[str]]) -> Self:
        index_items_in = check_optional_str_list(
            value=index_items_in,
            param_name="index_items_in",
        )
        self.params.index_items_in = index_items_in
        return self

    def having_index_items_in_top(self, index_top_n: Optional[int]) -> Self:
        index_top_n = check_optional_positive_int(
            value=index_top_n,
            param_name="index_top_n",
        )
        self.params.index_top_n = index_top_n
        return self

    def having_index_items_ordered_by(self, index_items_order_by: ItemOrderBy) -> Self:
        index_items_order_by = check_required_items_order_by_enum(
            value=index_items_order_by,
            param_name="index_items_order_by",
        )
        self.params.index_items_order_by = index_items_order_by
        return self

    def having_item_citations_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "item_citations_range"
        )
        self.params.item_citations_range = (start, end)
        return self

    def having_item_occurrences_between(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        start, end = check_required_open_ended_int_range(
            (start, end), "item_occurrences_range"
        )
        self.params.item_occurrences_range = (start, end)
        return self

    def having_items_in(self, item_list: Optional[list[str]]) -> Self:
        item_list = check_optional_str_list(
            value=item_list,
            param_name="items_in",
        )
        self.params.items_in = item_list
        return self

    def having_items_in_top(self, top_n: Optional[int]) -> Self:
        top_n = check_optional_positive_int(
            value=top_n,
            param_name="top_n",
        )
        self.params.top_n = top_n
        return self

    def having_items_ordered_by(self, items_order_by: ItemOrderBy) -> Self:
        items_order_by = check_required_items_order_by_enum(
            value=items_order_by,
            param_name="items_order_by",
        )
        self.params.items_order_by = items_order_by
        return self

    def having_items_per_year(self, items_per_year: int) -> Self:
        items_per_year = check_required_positive_int(
            value=items_per_year,
            param_name="items_per_year",
        )
        self.params.items_per_year = items_per_year
        return self

    def having_keys_ordered_by(self, keys_order_by: str) -> Self:
        keys_order_by = check_required_str(
            value=keys_order_by,
            param_name="keys_order_by",
        )
        self.params.keys_order_by = keys_order_by
        return self

    def having_maximum_occurrence(self, maximum_occurrence: int) -> Self:
        maximum_occurrence = check_required_positive_int(
            value=maximum_occurrence,
            param_name="maximum_occurrence",
        )
        self.params.maximum_occurrence = maximum_occurrence
        return self

    def having_n_chars(self, n_chars: int) -> Self:
        n_chars = check_required_positive_int(
            value=n_chars,
            param_name="n_chars",
        )
        self.params.n_chars = n_chars
        return self

    def having_n_contexts(self, n_contexts: int) -> Self:
        n_contexts = check_required_positive_int(
            value=n_contexts,
            param_name="n_contexts",
        )
        self.params.n_contexts = n_contexts
        return self

    def having_preferred_key(self, preferred_key: str) -> Self:
        preferred_key = check_required_str(
            value=preferred_key,
            param_name="preferred_key",
        )
        self.params.preferred_key = preferred_key
        return self

    def having_regex_flags(self, regex_flags: int) -> Self:
        regex_flags = check_required_non_negative_int(
            value=regex_flags,
            param_name="regex_flags",
        )
        self.params.regex_flags = regex_flags
        return self

    def having_regex_search(self, regex_search: bool) -> Self:
        regex_search = check_required_bool(
            value=regex_search,
            param_name="regex_search",
        )
        self.params.regex_search = regex_search
        return self

    def having_replacement(self, replacement: Optional[str]) -> Self:
        replacement = check_optional_str(
            value=replacement,
            param_name="replacement",
        )
        self.params.replacement = replacement
        return self

    def having_text_matching(self, pattern: Union[str, tuple[str, ...]]) -> Self:
        pattern = check_required_str_or_str_tuple(
            value=pattern,
            param_name="pattern",
        )
        self.params.pattern = pattern
        return self

    def having_variant_keys(self, variant_keys: tuple[str, ...]) -> Self:
        variant_keys = check_required_str_tuple(
            value=variant_keys,
            param_name="variant_keys",
        )
        self.params.variant_keys = variant_keys
        return self

    def having_word(self, word: str) -> Self:
        word = check_required_str(
            value=word,
            param_name="word",
        )
        self.params.word = word
        return self

    #
    # S
    #
    ## def showing_progress(self, progress):
    ##     self.params.show_progress = progress
    ##     return self

    #
    # U
    #
    def unit_of_analysis(self, unit_of_analysis) -> Self:
        self.params.unit_of_analysis = unit_of_analysis
        return self

    # ==========================================================================
    # USING_* → Parameters (HOW to analyze/display?)
    # ==========================================================================

    def using_association_index(self, normalization: AssociationIndex) -> Self:
        self.params.association_index = normalization
        return self

    def using_clustering_algorithm_or_dict(
        self, clustering_algorithm_or_dict: Optional[Union[str, dict]]
    ) -> Self:
        clustering_algorithm_or_dict = check_optional_str_or_dict(
            value=clustering_algorithm_or_dict,
            param_name="clustering_algorithm_or_dict",
        )
        self.params.clustering_algorithm_or_dict = clustering_algorithm_or_dict
        return self

    def having_citation_threshold(self, citation_threshold: int) -> Self:
        citation_threshold = check_required_non_negative_int(
            value=citation_threshold,
            param_name="citation_threshold",
        )
        self.params.citation_threshold = citation_threshold
        return self

    def using_colored_output(self, colored_output: bool) -> Self:
        colored_output = check_required_bool(
            value=colored_output,
            param_name="colored_output",
        )
        self.params.colored_output = colored_output
        return self

    def using_colored_stderr(self, colored_stderr: bool) -> Self:
        colored_stderr = check_required_bool(
            value=colored_stderr,
            param_name="colored_stderr",
        )
        self.params.colored_stderr = colored_stderr
        return self

    def using_similarity_cutoff(self, similarity_cutoff: float) -> Self:
        similarity_cutoff = check_required_positive_float(
            value=similarity_cutoff,
            param_name="similarity_cutoff",
        )
        self.params.similarity_cutoff = similarity_cutoff
        return self

    def having_occurrence_threshold(self, occurrence_threshold: int) -> Self:
        occurrence_threshold = check_required_positive_int(
            value=occurrence_threshold,
            param_name="occurrence_threshold",
        )
        self.params.occurrence_threshold = occurrence_threshold
        return self

    def using_decomposition_algorithm(
        self, decomposition_algorithm: Optional[BaseEstimator]
    ) -> Self:
        decomposition_algorithm = check_optional_base_estimator(
            value=decomposition_algorithm,
            param_name="decomposition_algorithm",
        )
        self.params.decomposition_algorithm = decomposition_algorithm
        return self

    def using_draw_arrows(self, draw_arrows: bool) -> Self:
        draw_arrows = check_required_bool(
            value=draw_arrows,
            param_name="draw",
        )
        self.params.draw_arrows = draw_arrows
        return self

    def using_axes_visible(self, axes_visible: bool) -> Self:
        axes_visible = check_required_bool(
            value=axes_visible,
            param_name="axes_visible",
        )
        self.params.axes_visible = axes_visible
        return self

    def using_baseline_periods(self, baseline_periods: int) -> Self:
        baseline_periods = check_required_positive_int(
            value=baseline_periods,
            param_name="baseline_periods",
        )
        self.params.baseline_periods = baseline_periods
        return self

    def using_binary_item_frequencies(self, frequencies: bool) -> Self:
        frequencies = check_required_bool(
            value=frequencies,
            param_name="binary_item_frequencies",
        )
        self.params.binary_item_frequencies = frequencies
        return self

    def using_cluster_coverages(self, cluster_coverages: Optional[list[str]]) -> Self:
        cluster_coverages = check_optional_str_list(
            value=cluster_coverages,
            param_name="cluster_coverages",
        )
        self.params.cluster_coverages = cluster_coverages
        return self

    def using_cluster_names(self, cluster_names: Optional[list[str]]) -> Self:
        cluster_names = check_optional_str_list(
            value=cluster_names,
            param_name="cluster_names",
        )
        self.params.cluster_names = cluster_names
        return self

    def using_color(self, color: str) -> Self:
        color = check_required_str(
            value=color,
            param_name="color",
        )
        self.params.color = color
        return self

    def using_colormap(self, colormap: str) -> Self:
        colormap = check_required_str(
            value=colormap,
            param_name="colormap",
        )
        self.params.colormap = colormap
        return self

    def using_contour_opacity(self, contour_opacity: float) -> Self:
        contour_opacity = check_required_float_0_1(
            value=contour_opacity,
            param_name="contour_opacity",
        )
        self.params.contour_opacity = contour_opacity
        return self

    def using_cumulative_sum(self, cumulative_sum: bool) -> Self:
        cumulative_sum = check_required_bool(
            value=cumulative_sum,
            param_name="cumulative_sum",
        )
        self.params.cumulative_sum = cumulative_sum
        return self

    def using_edge_colors(self, edge_colors: list[Any]) -> Self:
        edge_colors = check_required_color_list(
            value=edge_colors,
            param_name="edge_colors",
        )
        self.params.edge_colors = edge_colors
        return self

    def using_edge_similarity_threshold(self, edge_similarity_threshold: float) -> Self:
        edge_similarity_threshold = check_required_positive_float(
            value=edge_similarity_threshold,
            param_name="edge_similarity_threshold",
        )
        self.params.edge_similarity_threshold = edge_similarity_threshold
        return self

    def using_edge_top_n(self, edge_top_n: Optional[int]) -> Self:
        edge_top_n = check_optional_positive_int(
            value=edge_top_n,
            param_name="edge_top_n",
        )
        self.params.edge_top_n = edge_top_n
        return self

    def using_edge_opacity_range(self, min_opacity: float, max_opacity: float) -> Self:
        min_opacity, max_opacity = check_required_float_0_1_range(
            min_value=min_opacity,
            max_value=max_opacity,
            min_param_name="min_opacity",
            max_param_name="max_opacity",
        )
        self.params.edge_opacity_range = (min_opacity, max_opacity)
        return self

    def using_edge_width_range(self, min_width: float, max_width: float) -> Self:
        min_width, max_width = check_required_positive_float_range(
            range_tuple=(min_width, max_width),
            param_name="edge_width_range",
        )
        self.params.edge_width_range = (min_width, max_width)
        return self

    def using_edge_widths(
        self,
        edge_widths: Tuple[
            Union[float, int],
            Union[float, int],
            Union[float, int],
            Union[float, int],
        ],
    ) -> Self:
        values = cast(Tuple[float, float, float, float], edge_widths)
        values = check_tuple_of_ordered_four_floats(
            value=values,
            param_name="edge_widths",
        )
        self.params.edge_widths = values
        return self

    def using_initial_newline(self, initial_newline) -> Self:
        initial_newline = check_required_bool(
            value=initial_newline,
            param_name="initial_newline",
        )
        self.params.initial_newline = initial_newline
        return self

    def using_kernel_bandwidth(self, kernel_bandwidth: float) -> Self:
        kernel_bandwidth = check_required_positive_float(
            value=kernel_bandwidth,
            param_name="kernel_bandwidth",
        )
        self.params.kernel_bandwidth = kernel_bandwidth
        return self

    def using_line_color(self, line_color: Union[str, float, Sequence[float]]) -> Self:
        line_color = check_plotly_color(
            value=line_color,
            param_name="line_color",
        )
        self.params.line_color = line_color
        return self

    def using_line_width(self, line_width) -> Self:
        line_width = check_required_positive_float(
            value=line_width,
            param_name="line_width",
        )
        self.params.line_width = line_width
        return self

    def using_manifold_algorithm(
        self, manifold_algorithm: Optional[BaseEstimator]
    ) -> Self:
        manifold_algorithm = check_optional_base_estimator(
            value=manifold_algorithm,
            param_name="manifold_algorithm",
        )
        self.params.manifold_algorithm = manifold_algorithm
        return self

    def using_marker_size(self, marker_size: float) -> Self:
        marker_size = check_required_positive_float(
            value=marker_size,
            param_name="marker_size",
        )
        self.params.marker_size = marker_size
        return self

    def using_fuzzy_threshold(self, fuzzy_threshold: float) -> Self:
        fuzzy_threshold = check_required_non_negative_float(
            value=fuzzy_threshold,
            param_name="fuzzy_threshold",
        )
        self.params.fuzzy_threshold = fuzzy_threshold
        return self

    def using_minimum_number_of_clusters(self, minimum_number_of_clusters: int) -> Self:
        minimum_number_of_clusters = check_required_positive_int(
            value=minimum_number_of_clusters,
            param_name="minimum_number_of_clusters",
        )
        self.params.minimum_number_of_clusters = minimum_number_of_clusters
        return self

    def using_minimum_items_in_cluster(self, minimum_items_in_cluster: int) -> Self:
        minimum_items_in_cluster = check_required_positive_int(
            value=minimum_items_in_cluster,
            param_name="minimum_items_in_cluster",
        )
        self.params.minimum_items_in_cluster = minimum_items_in_cluster
        return self

    def using_node_colors(
        self, node_colors: List[Union[str, float, Sequence[float]]]
    ) -> Self:
        node_colors = check_required_color_list(
            value=node_colors,
            param_name="node_colors",
        )
        self.params.node_colors = node_colors
        return self

    def using_node_n_labels(self, node_n_labels: int) -> Self:
        node_n_labels = check_required_positive_int(
            value=node_n_labels,
            param_name="node_n_labels",
        )
        self.params.node_n_labels = node_n_labels
        return self

    def using_node_size(self, node_size: int) -> Self:
        node_size = check_required_positive_int(
            value=node_size,
            param_name="node_size",
        )
        self.params.node_size = node_size
        return self

    def using_node_size_range(self, min_size: int, max_size: int) -> Self:
        min_size, max_size = check_required_int_range(
            range_tuple=(min_size, max_size),
            param_name="node_size_range",
        )
        self.params.node_size_range = (min_size, max_size)
        return self

    def using_novelty_threshold(self, novelty_threshold: float) -> Self:
        novelty_threshold = check_required_float_0_1(
            value=novelty_threshold,
            param_name="novelty_threshold",
        )
        self.params.novelty_threshold = novelty_threshold
        return self

    def using_periods_with_at_least_one_record(self, periods: int) -> Self:
        periods = check_required_positive_int(
            value=periods,
            param_name="periods_with_at_least_one_record",
        )
        self.params.periods_with_at_least_one_record = periods
        return self

    def using_pie_hole(self, pie_hole: float) -> Self:
        pie_hole = check_required_float_0_1(
            value=pie_hole,
            param_name="pie_hole",
        )
        self.params.pie_hole = pie_hole
        return self

    def using_plot_dimensions(self, dim_x, dim_y) -> Self:
        self.params.plot_dimensions = (dim_x, dim_y)
        return self

    def using_plot_height(self, height) -> Self:
        self.params.plot_height = height
        return self

    def using_plot_width(self, width) -> Self:
        self.params.plot_width = width
        return self

    def using_ratio_threshold(self, threshold: float) -> Self:
        threshold = check_required_positive_float(
            value=threshold,
            param_name="ratio_threshold",
        )
        self.params.ratio_threshold = threshold
        return self

    def using_recent_periods(self, recent_periods: int) -> Self:
        recent_periods = check_required_positive_int(
            value=recent_periods,
            param_name="recent_periods",
        )
        self.params.recent_periods = recent_periods
        return self

    def using_spring_layout_iterations(self, spring_layout_iterations: int) -> Self:
        spring_layout_iterations = check_required_positive_int(
            value=spring_layout_iterations,
            param_name="spring_layout_iterations",
        )
        self.params.spring_layout_iterations = spring_layout_iterations
        return self

    def using_spring_layout_k(self, spring_layout_k: Optional[float]) -> Self:
        spring_layout_k = check_optional_positive_float(
            value=spring_layout_k,
            param_name="spring_layout_k",
        )
        self.params.spring_layout_k = spring_layout_k
        return self

    def using_spring_layout_seed(self, spring_layout_seed: int) -> Self:
        spring_layout_seed = check_required_int(
            value=spring_layout_seed,
            param_name="spring_layout_seed",
        )
        self.params.spring_layout_seed = spring_layout_seed
        return self

    def using_counters(self, counters: bool) -> Self:
        counters = check_required_bool(
            value=counters,
            param_name="counters",
        )
        self.params.counters = counters
        return self

    def using_textfont_color(
        self, textfont_color: Union[str, float, Sequence[float]]
    ) -> Self:
        textfont_color = check_plotly_color(
            value=textfont_color,
            param_name="textfont_color",
        )
        self.params.textfont_color = textfont_color
        return self

    def using_textfont_opacity(self, textfont_opacity: float) -> Self:
        textfont_opacity = check_required_float_0_1(
            value=textfont_opacity,
            param_name="textfont_opacity",
        )
        self.params.textfont_opacity = textfont_opacity
        return self

    def using_textfont_opacity_range(
        self, min_opacity: float, max_opacity: float
    ) -> Self:
        min_opacity, max_opacity = check_required_float_0_1_range(
            min_value=min_opacity,
            max_value=max_opacity,
            min_param_name="min_opacity",
            max_param_name="max_opacity",
        )
        self.params.textfont_opacity_range = (min_opacity, max_opacity)
        return self

    def using_textfont_size(self, textfont_size: float) -> Self:
        textfont_size = check_required_positive_float(
            value=textfont_size,
            param_name="textfont_size",
        )
        self.params.textfont_size = textfont_size
        return self

    def using_textfont_size_range(
        self, min_size: Union[float, int], max_size: Union[float, int]
    ) -> Self:
        min_size, max_size = check_required_positive_number_range(
            range_tuple=(min_size, max_size),
            param_name="textfont_size_range",
        )
        self.params.textfont_size_range = (min_size, max_size)
        return self

    def using_tfidf_norm(self, tfidf_norm: Optional[str]) -> Self:
        tfidf_norm = check_optional_str(
            value=tfidf_norm,
            param_name="tfidf_norm",
        )
        self.params.tfidf_norm = tfidf_norm
        return self

    def using_tfidf_smooth_idf(self, tfidf_smooth_idf: bool) -> Self:
        tfidf_smooth_idf = check_required_bool(
            value=tfidf_smooth_idf,
            param_name="tfidf_smooth_idf",
        )
        self.params.tfidf_smooth_idf = tfidf_smooth_idf
        return self

    def using_tfidf_sublinear_tf(self, tfidf_sublinear_tf: bool) -> Self:
        tfidf_sublinear_tf = check_required_bool(
            value=tfidf_sublinear_tf,
            param_name="tfidf_sublinear_tf",
        )
        self.params.tfidf_sublinear_tf = tfidf_sublinear_tf
        return self

    def using_tfidf_use_idf(self, tfidf_use_idf: bool) -> Self:
        tfidf_use_idf = check_required_bool(
            value=tfidf_use_idf,
            param_name="tfidf_use_idf",
        )
        self.params.tfidf_use_idf = tfidf_use_idf
        return self

    def using_title_text(self, title_text: Optional[str]) -> Self:
        title_text = check_optional_str(
            value=title_text,
            param_name="title_text",
        )
        self.params.title_text = title_text
        return self

    def using_top_items_by_theme(self, top_items_by_theme: int) -> Self:
        top_items_by_theme = check_required_positive_int(
            value=top_items_by_theme,
            param_name="top_items_by_theme",
        )
        self.params.top_items_by_theme = top_items_by_theme
        return self

    def using_total_records_threshold(self, total_records_threshold: int) -> Self:
        total_records_threshold = check_required_positive_int(
            value=total_records_threshold,
            param_name="total_records_threshold",
        )
        self.params.total_records_threshold = total_records_threshold
        return self

    def using_xaxes_range(self, x_min: Optional[float], x_max: Optional[float]) -> Self:

        if x_min is None and x_max is None:
            self.params.xaxes_range = None
            return self
        x_min, x_max = check_required_float_range(
            min_value=cast(float, x_min),
            max_value=cast(float, x_max),
            min_param_name="x_min",
            max_param_name="x_max",
        )
        self.params.xaxes_range = (x_min, x_max)
        return self

    def using_xaxes_title_text(self, xaxes_title_text: Optional[str]) -> Self:
        xaxes_title_text = check_optional_str(
            value=xaxes_title_text,
            param_name="xaxes_title_text",
        )
        self.params.xaxes_title_text = xaxes_title_text
        return self

    def using_yaxes_range(self, y_min: Optional[float], y_max: Optional[float]) -> Self:

        if y_min is None and y_max is None:
            self.params.yaxes_range = None
            return self
        y_min, y_max = check_required_float_range(
            min_value=cast(float, y_min),
            max_value=cast(float, y_max),
            min_param_name="y_min",
            max_param_name="y_max",
        )
        self.params.yaxes_range = (y_min, y_max)
        return self

    def using_yaxes_title_text(self, yaxes_title_text: Optional[str]) -> Self:
        yaxes_title_text = check_optional_str(
            value=yaxes_title_text,
            param_name="yaxes_title_text",
        )
        self.params.yaxes_title_text = yaxes_title_text
        return self

    def using_yshift(self, yshift: float) -> Self:
        yshift = check_required_float(
            value=yshift,
            param_name="yshift",
        )
        self.params.yshift = yshift
        return self

    def using_word_length(self, word_length: int) -> Self:
        word_length = check_required_positive_int(
            value=word_length,
            param_name="word_length",
        )
        self.params.word_length = word_length
        return self

    def using_zotero_api_key(self, zotero_api_key: str) -> Self:
        zotero_api_key = check_required_str(
            value=zotero_api_key,
            param_name="api_key",
        )
        self.params.zotero_api_key = zotero_api_key
        return self

    def using_zotero_library_id(self, zotero_library_id: str) -> Self:
        zotero_library_id = check_required_str(
            value=zotero_library_id,
            param_name="library_id",
        )
        self.params.zotero_library_id = zotero_library_id
        return self

    def using_zotero_library_type(self, zotero_library_type: str) -> Self:
        zotero_library_type = check_required_str(
            value=zotero_library_type,
            param_name="library_type",
        )
        self.params.zotero_library_type = zotero_library_type
        return self

    # ==========================================================================
    # WITH_* → Configuration (WHAT to analyze?)
    # ==========================================================================

    def with_citation_unit(self, citation_unit: CitationUnit) -> Self:
        if not isinstance(citation_unit, CitationUnit):
            raise TypeError("citation_unit must be an instance of CitationUnit enum")
        self.params.citation_unit = citation_unit
        return self

    def with_co_citation_unit(self, co_citation_unit: CoCitationUnit) -> Self:
        if not isinstance(co_citation_unit, CoCitationUnit):
            raise TypeError(
                "co_citation_unit must be an instance of CoCitationUnit enum"
            )
        self.params.co_citation_unit = co_citation_unit
        return self

    def with_coupling_unit(self, coupling_unit: CouplingUnit) -> Self:
        if not isinstance(coupling_unit, CouplingUnit):
            raise TypeError("coupling_unit must be an instance of CouplingUnit enum")
        self.params.coupling_unit = coupling_unit
        return self

    def with_column(self, column: str) -> Self:
        column = check_required_str(
            value=column,
            param_name="column",
        )
        self.params.column = column
        return self

    def with_column_field(self, column_field: Field) -> Self:
        column_field = check_required_corpus_field_enum(
            value=column_field,
            param_name="column_field",
        )
        self.params.column_field = column_field
        return self

    def with_core_area(self, core_area: Optional[str]) -> Self:
        core_area = check_optional_str(
            value=core_area,
            param_name="core_area",
        )
        self.params.core_area = core_area
        return self

    def with_correlation_method(self, correlation_method: Correlation) -> Self:
        if not isinstance(correlation_method, Correlation):
            raise TypeError(
                "correlation_method must be an instance of Correlation enum"
            )
        self.params.correlation_method = correlation_method
        return self

    # def with_index_and_column_field(self, index_and_column_field: Field) -> Self:
    #     index_and_column_field = check_required_corpus_field_enum(
    #         value=index_and_column_field,
    #         param_name="index_and_column_field",
    #     )
    #     self.params.index_and_column_field = index_and_column_field
    #     return self

    def with_index_field(self, index_field: Field) -> Self:
        index_field = check_required_corpus_field_enum(
            value=index_field,
            param_name="index_field",
        )
        self.params.index_field = index_field
        return self

    # def with_field(self, field: CorpusField) -> Self:
    #     field = check_required_corpus_field_enum(
    #         value=field,
    #         param_name="field",
    #     )
    #     self.params.field = field
    #     return self

    def with_cross_field(self, field: Field) -> Self:
        field = check_required_corpus_field_enum(
            value=field,
            param_name="cross_field",
        )
        self.params.cross_field = field
        return self

    def with_params(self, params) -> Self:
        self.update(**params.__dict__)
        return self

    def with_plotting_column(self, plotting_column: Any) -> Self:
        self.params.plotting_column = plotting_column
        return self

    def with_query_expression(self, query_expression: str) -> Self:
        query_expression = check_required_str(
            value=query_expression,
            param_name="query_expression",
        )
        self.params.query_expression = query_expression
        return self

    def with_source_field(self, field: Field) -> Self:
        field = check_required_corpus_field_enum(
            value=field,
            param_name="source_field",
        )
        self.params.source_field = field
        return self

    def with_source_fields(self, fields: tuple[Field, ...]) -> Self:
        for field in fields:
            check_required_corpus_field_enum(
                value=field,
                param_name="source_fields",
            )
        self.params.source_fields = fields
        return self

    def with_target_field(self, field: Field) -> Self:
        field = check_required_corpus_field_enum(
            value=field,
            param_name="target_field",
        )
        self.params.target_field = field
        return self

    def with_thesaurus_file(self, thesaurus_file: str) -> Self:
        thesaurus_file = check_required_str(
            value=thesaurus_file,
            param_name="thesaurus_file",
        )
        self.params.thesaurus_file = thesaurus_file
        return self

    def with_time_window(self, time_window: int) -> Self:
        time_window = check_required_positive_int(
            value=time_window,
            param_name="time_window",
        )
        self.params.time_window = time_window
        return self

    def with_transformation_function(
        self, transformation_function: Optional[Callable[[Any], Any]]
    ) -> Self:
        self.params.transformation_function = transformation_function
        return self

    # ==========================================================================
    # WHERE_* → Data filtering (WHICH records?)
    # ==========================================================================

    # def where_database(self, database: str) -> Self:
    #     database = internal__check_required_str(
    #         value=database,
    #         param_name="database",
    #     )
    #     self.params.database = database
    #     return self

    def where_record_citations_range(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        self.params.record_citations_range = check_required_open_ended_int_range(
            (start, end), "record_citations_range"
        )
        return self

    def where_record_years_range(
        self, start: Optional[int], end: Optional[int]
    ) -> Self:
        (start, end) = check_required_open_ended_int_range(
            (start, end), "record_years_range"
        )
        self.params.record_years_range = (start, end)
        return self

    def where_records_match(
        self, records_match: Optional[Dict[Field, List[str]]]
    ) -> Self:
        self.params.records_match = records_match
        return self

    def where_records_ordered_by(self, records_order_by: RecordOrderBy) -> Self:
        if not isinstance(records_order_by, RecordOrderBy):
            raise TypeError(
                "records_order_by must be an instance of RecordsOrderBy enum"
            )
        self.params.records_order_by = records_order_by
        return self

    def where_root_directory(self, root_directory: str) -> Self:
        root_directory = check_required_str(
            value=root_directory,
            param_name="root_directory",
        )
        self.params.root_directory = root_directory
        return self
