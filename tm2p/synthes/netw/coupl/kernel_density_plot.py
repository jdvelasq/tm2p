"""
Network Density Plot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.synthes.networks.coupling.kernel_density_plot_1.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.networks.coupling.kernel_density_plot_2.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.networks.coupling.kernel_density_plot_3.html"
    height="800px" width="100%" frameBorder="0"></iframe>

    <iframe src="../_generated/px.synthes.networks.coupling.kernel_density_plot_4.html"
    height="800px" width="100%" frameBorder="0"></iframe>



Smoke tests:
    >>> from tm2p import CouplingUnit
    >>> from tm2p.synthes.netw.coupl import KernelDensityPlot
    >>> fig = (
    ...     KernelDensityPlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     # DENSITY:
    ...     .using_kernel_bandwidth(0.1)
    ...     .using_colormap("Aggrnyl")
    ...     .using_contour_opacity(0.6)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.networks.coupling.kernel_density_plot_1.html")

    >>> fig = (
    ...     KernelDensityPlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     # DENSITY:
    ...     .using_kernel_bandwidth(0.1)
    ...     .using_colormap("Aggrnyl")
    ...     .using_contour_opacity(0.6)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.networks.coupling.kernel_density_plot_2.html")

    >>> fig = (
    ...     KernelDensityPlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.ORG)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     # DENSITY:
    ...     .using_kernel_bandwidth(0.1)
    ...     .using_colormap("Aggrnyl")
    ...     .using_contour_opacity(0.6)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.networks.coupling.kernel_density_plot_3.html")

    >>> fig = (
    ...     KernelDensityPlot()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.ORG)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict("louvain")
    ...     #
    ...     # NETWORK:
    ...     .using_spring_layout_k(None)
    ...     .using_spring_layout_iterations(30)
    ...     .using_spring_layout_seed(0)
    ...     #
    ...     # DENSITY:
    ...     .using_kernel_bandwidth(0.1)
    ...     .using_colormap("Aggrnyl")
    ...     .using_contour_opacity(0.6)
    ...     .using_textfont_size_range(10, 20)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> fig.write_html("docsrc/_generated/px.synthes.networks.coupling.kernel_density_plot_4.html")






"""

from tm2p import CouplingUnit, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.synthes.netw.coupl._intern.doc import KernelDensityPlot as DocDensityPlot
from tm2p.synthes.netw.coupl._intern.other import KernelDensityPlot as OtherDensityPlot


class KernelDensityPlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.coupling_unit == CouplingUnit.DOC:
            DensityPlot = DocDensityPlot
        else:
            DensityPlot = OtherDensityPlot

        return (
            DensityPlot()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )
