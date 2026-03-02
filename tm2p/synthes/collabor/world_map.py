"""
World Map
===============================================================================


Smoke tests:
    >>> from tm2p.analyze.metrics.collaboration import WorldMap

    >>> # Creates, configure, and plots a world map.
    >>> plotter = (
    ...     WorldMap()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ... )
    >>> plot = plotter.run()
    >>> plot.write_html("docsrc/_generated/px.database.metrics.collaboration.world_map.html")

.. raw:: html

    <iframe src="../_generated/px.database.metrics.collaboration.world_map.html"
    height="600px" width="100%" frameBorder="0"></iframe>



"""

import plotly.express as px  # type: ignore

from tm2p import Field, ItemsOrderBy
from tm2p._intern import ParamsMixin
from tm2p.discov.co_occur_matrix._intern.matrix import Matrix as CoOccurrenceDataFrame


class WorldMap(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__build_collaboration_data_frame(self):

        # Builds a collaboration data frame with columns "rows", "columns", and "OCC"
        collaboration = (
            CoOccurrenceDataFrame()
            .update(**self.params.__dict__)
            .with_source_field(Field.CTRY)
            .update(terms_order_by=ItemsOrderBy.OCC)
            .run()
        )

        collaboration = collaboration[collaboration["rows"] != collaboration["columns"]]
        collaboration["row"] = collaboration["rows"].map(
            lambda x: " ".join(x.split()[:-1])
        )
        collaboration["column"] = collaboration["columns"].map(
            lambda x: " ".join(x.split()[:-1])
        )

        collaboration["pair"] = list(zip(collaboration.row, collaboration.column))
        collaboration["line"] = list(range(len(collaboration)))
        collaboration = collaboration[["pair", "line"]]
        collaboration = collaboration.explode("pair")

        self.collaboration = collaboration

    # -------------------------------------------------------------------------
    def internal__plot_world_map(self):

        fig = px.line_geo(
            self.collaboration,
            locations="pair",
            locationmode="country names",
            color="line",
            color_discrete_sequence=["darkslategray"],
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(l=1, r=1, t=1, b=1),
        )

        fig.update_geos(
            showcountries=True,
            landcolor="lightgray",
            countrycolor="Black",
            lataxis_showgrid=False,
            lonaxis_showgrid=False,
        )

        self.fig = fig

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__build_collaboration_data_frame()
        self.internal__plot_world_map()

        return self.fig


#
