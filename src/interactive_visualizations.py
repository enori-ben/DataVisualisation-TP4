from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import folium


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "cleaned_world_bank.csv"
GEOJSON_FILE = ROOT_DIR / "data" / "countries.geo.json"
RESULTS_DIR = ROOT_DIR / "results"


def load_data():
    """Load the cleaned dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run data_preprocessing.py first."
        )

    return pd.read_csv(DATA_FILE)


def create_gdp_time_series(df):
    """Compare GDP per capita trends in Germany and Algeria."""

    countries = ["Germany", "Algeria"]

    data = df[df["Country"].isin(countries)].copy()
    data = data.dropna(subset=["Year", "GDP_Per_Capita"])

    if data.empty:
        raise ValueError("No GDP data found for Germany and Algeria.")

    fig = px.line(
        data,
        x="Year",
        y="GDP_Per_Capita",
        color="Country",
        markers=True,
        title="GDP per Capita: Germany vs Algeria (2000–2023)",
        labels={
            "Year": "Year",
            "GDP_Per_Capita": "GDP per Capita (current US$)",
            "Country": "Country"
        },
        hover_data=["Population", "Life_Expectancy"]
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        xaxis_title="Year",
        yaxis_title="GDP per Capita (current US$)"
    )

    fig.write_html(
        RESULTS_DIR / "05_interactive_gdp.html",
        include_plotlyjs=True
    )


def create_life_expectancy_map(df):
    """Create a Folium choropleth map for the latest available year."""

    if not GEOJSON_FILE.exists():
        raise FileNotFoundError(
            "GeoJSON file not found: data/countries.geo.json"
        )

    latest_year = int(df["Year"].max())

    latest_data = df[df["Year"] == latest_year].copy()
    latest_data = latest_data.dropna(subset=["Life_Expectancy"])

    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        geojson_data = json.load(file)

    country_values = (
        latest_data.set_index("ISO3")[
            ["Country", "Life_Expectancy"]
        ].to_dict("index")
    )

    # Add country information to GeoJSON properties.
    for feature in geojson_data["features"]:
        iso3 = feature.get("id")
        properties = feature.setdefault("properties", {})

        country = country_values.get(iso3)

        if country:
            properties["Country"] = country["Country"]
            properties["Life_Expectancy"] = round(
                country["Life_Expectancy"], 2
            )
        else:
            properties["Country"] = properties.get("name", "Unknown")
            properties["Life_Expectancy"] = "No data"

    world_map = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="OpenStreetMap"
    )

    folium.Choropleth(
        geo_data=geojson_data,
        data=latest_data,
        columns=["ISO3", "Life_Expectancy"],
        key_on="feature.id",
        fill_color="YlGnBu",
        fill_opacity=0.75,
        line_opacity=0.2,
        legend_name=f"Life Expectancy (years) - {latest_year}",
        nan_fill_color="lightgray"
    ).add_to(world_map)

    folium.GeoJson(
        geojson_data,
        name="Country details",
        tooltip=folium.GeoJsonTooltip(
            fields=["Country", "Life_Expectancy"],
            aliases=["Country:", "Life Expectancy:"],
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=["Country", "Life_Expectancy"],
            aliases=["Country:", "Life Expectancy:"],
            localize=True
        )
    ).add_to(world_map)

    folium.LayerControl().add_to(world_map)

    world_map.save(
        RESULTS_DIR / "06_life_expectancy_map.html"
    )


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned dataset...")
    df = load_data()

    print("Creating interactive GDP time series...")
    create_gdp_time_series(df)

    print("Creating life expectancy choropleth map...")
    create_life_expectancy_map(df)

    print("\nInteractive visualizations generated successfully.")


if __name__ == "__main__":
    main()
