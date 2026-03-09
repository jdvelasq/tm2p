"""
LifeCyclePlot
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.life_cycle.life_cycle_plot.html"
    height="800px" width="100%" frameBorder="0"></iframe>


Smoke test:
    >>> from tm2p.discov.life_cycle import LifeCyclePlot
    >>> fig = (
    ...     LifeCyclePlot()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/regtech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> type(fig).__name__
    'Figure'
    >>> fig.write_html("docsrc/_generated/px.discov.life_cycle.life_cycle_plot.html")


"""

import numpy as np
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin

from ._intern.compute_model_parameters import compute_model_parameters
from ._intern.logistic_derivative import logistic_derivative


class LifeCyclePlot(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        K, r, t0, years, annual_counts, _ = compute_model_parameters(params=self.params)
        peak_year = round(t0)
        peak_annual = (K * r) / 4

        # Extended axis centered on peak year
        half_window = max(peak_year - years.min(), years.max() - peak_year) * 1.3
        half_window = max(half_window, 15)
        t_extended = np.linspace(peak_year - half_window, peak_year + half_window, 500)
        t_10 = t0 - np.log(9) / r
        t_90 = t0 + np.log(9) / r

        # --- DataFrames for px ---
        df_fit = pd.DataFrame(
            {
                "Year": t_extended,
                "Pubs": logistic_derivative(t_extended, K, r, t0),
                "Series": "Logistic fit",
            }
        )

        df_obs = pd.DataFrame(
            {"Year": years, "Pubs": annual_counts, "Series": "Observed"}
        )

        # --- Base figure from px.line on fitted curve ---
        fig = px.line(
            df_fit,
            x="Year",
            y="Pubs",
            title=self.params.title_text,
            labels={
                "Pubs": "Annual Publications",
                "Year": "Year",
            },
            color_discrete_map={
                "Logistic fit": "#2c7bb6",
            },
            color="Series",
        )

        # --- Add observed bars and points via go traces ---
        fig.add_trace(
            go.Bar(
                x=df_obs["Year"],
                y=df_obs["Pubs"],
                name="Observed",
                marker_color="rgba(44,123,182,0.25)",
                marker_line=dict(color="rgba(44,123,182,0.6)", width=1),
                hovertemplate="Observed: <b>%{y}</b><extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df_obs["Year"],
                y=df_obs["Pubs"],
                mode="markers",
                name="Observed",
                marker=dict(color="#2c7bb6", size=7, line=dict(color="white", width=1)),
                showlegend=False,
                hovertemplate="Observed: <b>%{y}</b><extra></extra>",
            )
        )

        # --- Phase shading ---
        for x0, x1, color, label, font_color in [
            (
                peak_year - half_window,
                t_10,
                "rgba(173,216,230,0.15)",
                "Emergence",
                "#5b8fa8",
            ),
            (t_10, t_90, "rgba(144,238,144,0.15)", "Growth", "#3a7d44"),
            (
                t_90,
                peak_year + half_window,
                "rgba(255,200,100,0.15)",
                "Maturity / Decline",
                "#b5651d",
            ),
        ]:
            fig.add_vrect(
                x0=x0,
                x1=x1,
                fillcolor=color,
                line_width=0,
                annotation_text=label,
                annotation_position="top left",
                annotation_font={
                    "size": 11,
                    "color": font_color,
                },
            )

        # --- Peak line + annotation ---
        fig.add_vline(
            x=peak_year,
            line={
                "color": "#d73027",
                "width": 2,
                "dash": "dash",
            },
        )
        fig.add_hline(
            y=peak_annual,
            line={"color": "rgba(215,48,39,0.3)", "width": 1.5, "dash": "dot"},
        )

        fig.add_annotation(
            x=peak_year,
            y=peak_annual,
            text=f"<b>Peak: {peak_year}</b><br>{peak_annual:.0f} pubs/yr",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#d73027",
            arrowwidth=1.5,
            ax=50,
            ay=-45,
            bgcolor="white",
            bordercolor="#d73027",
            borderwidth=1.5,
            borderpad=5,
            font=dict(size=12, color="#d73027"),
        )

        # --- Layout ---
        fig.update_traces(line={"width": 3}, selector={"name": "Logistic fit"})
        fig.update_layout(
            xaxis={
                "range": [peak_year - half_window, peak_year + half_window],
                "showgrid": True,
                "gridcolor": "rgba(200,200,200,0.3)",
                "tickformat": "d",
                "zeroline": False,
            },
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(200,200,200,0.3)",
                zeroline=False,
                rangemode="tozero",
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(200,200,200,0.5)",
                borderwidth=1,
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            bargap=0.15,
            hovermode="x unified",
            # width=900,
            # height=500,
            margin=dict(t=80, b=60, l=70, r=40),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )

        return fig
