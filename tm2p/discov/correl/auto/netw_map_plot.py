"""
NetworkMapPlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.correl.auto.netw_map_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> # grey colors: https://www.w3schools.com/colors/colors_shades.asp
    >>> from tm2p import ItemOrderBy, Field, Correlation
    >>> from tm2p.discov.correl.auto import NetworkMapPlot
    >>> plot = (
    ...     NetworkMapPlot()
    ...     #
    ...     # FIELD:
    ...     .with_source_field(Field.AUTHKW_NORM)
    ...     .having_items_in_top(10)
    ...     .having_items_ordered_by(ItemOrderBy.OCC)
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # CORRELATION:
    ...     .with_correlation_method(Correlation.PEARSON)
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     .using_edge_colors(("#7793a5", "#7793a5", "#7793a5", "#7793a5"))
    ...     .using_edge_similarity_threshold(0.01)
    ...     .using_edge_top_n(None)
    ...     .using_edge_widths((2, 2, 4, 6))
    ...     #
    ...     .using_node_colors(("#7793a5",))
    ...     .using_node_size_range(30, 70)
    ...     #
    ...     .using_node_n_labels(5)
    ...     .using_textfont_opacity_range(0.35, 1.00)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     .using_xaxes_range(None, None)
    ...     .using_yaxes_range(None, None)
    ...     .using_axes_visible(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> plot.write_html("docsrc/_generated/px.discov.correl.auto.netw_map_plot.html")



"""

import pandas as pd  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

from tm2p import Correlation
from tm2p._intern import ParamsMixin

from .._intern import plot_correl_map
from .matrix import Matrix


class NetworkMapPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        df = Matrix().update(**self.params.__dict__).run()

        if self.params.correlation_method != Correlation.COSINE:
            df = pd.DataFrame(
                cosine_similarity(df),
                index=df.index,
                columns=df.columns,
            )

        return plot_correl_map(self.params, df)
