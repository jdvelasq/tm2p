"""
CumulativeGrowthCurve
===============================================================================

.. raw:: html

    <iframe src="../_generated/px.discov.life_cycle.cumulative_growth_curve.html"
    height="800px" width="100%" frameBorder="0"></iframe>


Smoke test:
    >>> from tm2p.discov.life_cycle import CumulativeGrowthCurve
    >>> fig = (
    ...     CumulativeGrowthCurve()
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
    >>> fig.write_html("docsrc/_generated/px.discov.life_cycle.cumulative_growth_curve.html")


"""

import numpy as np
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore

from tm2p._intern import ParamsMixin

from ._intern.compute_model_parameters import compute_model_parameters
from ._intern.logistic import logistic


class CumulativeGrowthCurve(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        K, r, t0, years, annual_counts, cumulative = compute_model_parameters(
            params=self.params
        )

        peak_year = round(t0)

        # Extended x-axis
        half_window = max(peak_year - years.min(), years.max() - peak_year) * 1.3
        half_window = max(half_window, 15)
        t_extended = np.linspace(peak_year - half_window, peak_year + half_window, 500)

        # --- DataFrames ---
        df_fit = pd.DataFrame(
            {
                "Year": t_extended,
                "Cumulative": logistic(t_extended, K, r, t0),
                "Series": "Logistic fit",
            }
        )

        df_obs = pd.DataFrame(
            {"Year": years, "Cumulative": cumulative, "Series": "Observed"}
        )

        # --- Base figure ---
        fig = px.line(
            df_fit,
            x="Year",
            y="Cumulative",
            title=self.params.title_text,
            labels={"Cumulative": "Cumulative Publications", "Year": "Year"},
            color="Series",
            color_discrete_map={"Logistic fit": "#2c7bb6"},
        )

        # --- Observed dots ---
        fig.add_trace(
            go.Scatter(
                x=df_obs["Year"],
                y=df_obs["Cumulative"],
                mode="markers",
                name="Observed",
                marker=dict(color="#2c7bb6", size=7, line=dict(color="white", width=1)),
                hovertemplate="Year: %{x}<br>Cumulative: <b>%{y:,.0f}</b><extra></extra>",
            )
        )

        # --- K asymptote ---
        fig.add_hline(
            y=K,
            line=dict(color="rgba(215,48,39,0.5)", width=1.5, dash="dash"),
            annotation_text=f"K = {K:,.0f}",
            annotation_position="right",
            annotation_font=dict(size=11, color="#d73027"),
        )

        # --- Inflection point ---
        fig.add_trace(
            go.Scatter(
                x=[peak_year],
                y=[K / 2],
                mode="markers",
                name=f"Inflection ({peak_year})",
                marker=dict(
                    color="#d73027",
                    size=11,
                    symbol="diamond",
                    line=dict(color="white", width=1.5),
                ),
                hovertemplate=f"Inflection: {peak_year}<br>Cumulative: {K/2:,.0f}<extra></extra>",
            )
        )

        fig.add_annotation(
            x=peak_year,
            y=K / 2,
            text=f"<b>Inflection: {peak_year}</b><br>{K/2:,.0f} pubs",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#d73027",
            arrowwidth=1.5,
            ax=70,
            ay=-40,
            bgcolor="white",
            bordercolor="#d73027",
            borderwidth=1.5,
            borderpad=5,
            font=dict(size=12, color="#d73027"),
        )

        # --- Layout ---
        fig.update_traces(line=dict(width=3), selector=dict(name="Logistic fit"))
        fig.update_layout(
            xaxis=dict(
                range=[peak_year - half_window, peak_year + half_window],
                showgrid=True,
                gridcolor="rgba(200,200,200,0.3)",
                tickformat="d",
                zeroline=False,
            ),
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
            hovermode="x unified",
            width=900,
            height=500,
            margin=dict(t=80, b=60, l=70, r=80),
            title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        )

        return fig
