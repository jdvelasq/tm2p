import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore


def world_map(params, df):

    #
    # Variables
    colormap = params.colormap
    hover_data = [col for col in df.columns if col not in ["country", "iso_alpha"]]
    metric = params.items_order_by.value
    title_text = params.title_text

    #
    # Load worl map data
    world_map_data = px.data.gapminder()[["country", "continent", "iso_alpha"]]
    world_map_data = world_map_data.drop_duplicates()

    #
    # Adds to world_map_data the Russia, Greenland, and Antarctica
    world_map_data = pd.concat(
        [
            world_map_data,
            pd.DataFrame(
                {
                    "country": ["Russia", "Greenland", "Antarctica"],
                    "continent": ["Asia", "North America", "Antarctica"],
                    "iso_alpha": ["RUS", "GRL", "ATA"],
                }
            ),
        ],
        ignore_index=True,
    )

    world_map_data = world_map_data.reset_index(drop=True)
    world_map_data.index = pd.Index(world_map_data.country.to_list())

    #
    # Plots the world map
    df.index = df.index.rename("country")
    df = df.sort_index()

    world_map_data = world_map_data.join(df, how="left")
    world_map_data = world_map_data.fillna(0)

    world_map_data["plot_metric"] = world_map_data[metric].where(
        world_map_data[metric] > 0, pd.NA
    )
    max_metric = max(1, world_map_data[metric].max())

    fig = px.choropleth(
        world_map_data,
        locations="iso_alpha",
        color="plot_metric",
        hover_name="country",
        hover_data=hover_data,
        range_color=(1, max_metric),
        color_continuous_scale=colormap,
        color_discrete_map={0: "gray"},
        scope="world",
    )

    fig.update_geos(
        # projection_type="natural earth",
        projection_rotation=dict(lon=10),
        showframe=False,
        showland=True,
        landcolor="whitesmoke",
        showcountries=True,
        countrycolor="black",
        countrywidth=0.7,
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.01,
            xanchor="left",
            y=0.98,
            yanchor="top",
            pad=dict(t=0, b=0),
        ),
        margin=dict(t=40, l=0, r=0, b=0),
    )

    return fig
