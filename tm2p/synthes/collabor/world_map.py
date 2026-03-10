"""
WorldMap
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.synthes.collabor.world_map.html"
    height="450" width="100%" frameBorder="0"></iframe>


Smoke tests:
    >>> from tm2p import Field, ItemOrderBy
    >>> from tm2p.synthes.collabor import WorldMap
    >>> plotter = (
    ...     WorldMap()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ... )
    >>> plot = plotter.run()
    >>> plot.write_html("docsrc/_generated/px.synthes.collabor.world_map.html")




"""

import plotly.express as px  # type: ignore

from tm2p import Field, ItemOrderBy
from tm2p._intern import ParamsMixin
from tm2p.anal.metrics import WorldMap as OccWorldMap
from tm2p.discov.co_occur_matrix.matrix_list import MatrixList as CoOccurrenceDataFrame


class WorldMap(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__build_collaboration_data_frame(self):

        df = (
            CoOccurrenceDataFrame()
            .update(**self.params.__dict__)
            .with_source_field(Field.CTRY)
            .update(terms_order_by=ItemOrderBy.OCC)
            .run()
        )

        df = df[df["rows"] < df["columns"]]
        df = df[df["OCC"] > 0]
        df["row"] = df["rows"].map(lambda x: " ".join(x.split()[:-1]))
        df["column"] = df["columns"].map(lambda x: " ".join(x.split()[:-1]))

        df["pair"] = list(zip(df.row, df.column))
        df["line"] = list(range(len(df)))
        df = df[["pair", "line", "OCC"]]
        df = df.explode("pair")

        return df

    # -------------------------------------------------------------------------
    def internal__plot_world_map(self, fig, df):

        line_occ = df[["line", "OCC"]].drop_duplicates("line").set_index("line")["OCC"]

        occ_min = float(line_occ.min())
        occ_max = float(line_occ.max())

        def _scale_width(occ):
            min_w, max_w = 1.0, 12.0
            if occ_max == occ_min:
                return 2.0
            return min_w + (float(occ) - occ_min) * (max_w - min_w) / (
                occ_max - occ_min
            )

        def _scale_opacity(occ):
            min_op, max_op = 0.2, 1.0
            if occ_max == occ_min:
                return 0.5
            return min_op + (float(occ) - occ_min) * (max_op - min_op) / (
                occ_max - occ_min
            )

        line_fig = px.line_geo(
            df,
            locations="pair",
            locationmode="country names",
            # color="line",
            line_group="line",
        )

        line_fig.update_traces(
            mode="lines",
            # line=dict(color="darkslategray", width=1.2),
            hoverinfo="skip",
            showlegend=False,
        )

        # for trace in line_fig.data:
        #     fig.add_trace(trace)

        for trace in line_fig.data:
            try:
                line_id = int(trace.name)  # type: ignore
            except (TypeError, ValueError):
                line_id = None

            occ = line_occ.get(line_id, occ_min)
            trace.line = dict(color="black", width=_scale_width(occ))  # type: ignore
            trace.opacity = _scale_opacity(occ)  # type: ignore
            fig.add_trace(trace)

        return fig

    # -------------------------------------------------------------------------
    def run(self):

        fig = (
            OccWorldMap()
            .update(**self.params.__dict__)
            .with_source_field(Field.CTRY)
            .run()
        )
        df = self.internal__build_collaboration_data_frame()
        fig = self.internal__plot_world_map(fig, df)

        return fig


#
