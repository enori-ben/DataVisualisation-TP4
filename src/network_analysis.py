from pathlib import Path

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "cleaned_world_bank.csv"
RESULTS_DIR = ROOT_DIR / "results"


def load_data():
    """Load the cleaned World Bank dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run data_preprocessing.py first."
        )

    return pd.read_csv(DATA_FILE)


def build_regional_graph(df):
    """Build a hierarchy: World -> Regions -> Countries."""

    latest_year = int(df["Year"].max())

    latest_data = df[df["Year"] == latest_year].copy()

    latest_data = latest_data.dropna(
        subset=["ISO3", "Region", "Country", "Population"]
    )

    latest_data = latest_data.drop_duplicates(subset=["ISO3"])

    graph = nx.DiGraph()

    graph.add_node(
        "World",
        node_type="world",
        label="World",
        level=0
    )

    for region in sorted(latest_data["Region"].unique()):
        region_id = f"Region: {region}"

        graph.add_node(
            region_id,
            node_type="region",
            label=region,
            level=1
        )

        graph.add_edge("World", region_id)

        region_data = latest_data[
            latest_data["Region"] == region
        ]

        for _, row in region_data.iterrows():
            country_id = f"Country: {row['ISO3']}"

            graph.add_node(
                country_id,
                node_type="country",
                label=row["Country"],
                population=row["Population"],
                level=2
            )

            graph.add_edge(region_id, country_id)

    return graph, latest_year


def draw_regional_graph(graph, latest_year):
    """Draw and save the regional hierarchy."""

    positions = nx.multipartite_layout(
        graph,
        subset_key="level",
        align="vertical"
    )

    colors = []
    sizes = []
    labels = {}

    for node, attributes in graph.nodes(data=True):
        node_type = attributes["node_type"]
        labels[node] = attributes["label"]

        if node_type == "world":
            colors.append("gold")
            sizes.append(2200)

        elif node_type == "region":
            colors.append("skyblue")
            sizes.append(1300)

        else:
            colors.append("lightgreen")

            population = attributes.get("population", 0)
            sizes.append(max(80, min(population / 1000000, 900)))

    plt.figure(figsize=(24, 18))

    nx.draw(
        graph,
        positions,
        labels=labels,
        with_labels=True,
        node_color=colors,
        node_size=sizes,
        font_size=5,
        font_weight="bold",
        arrows=False,
        edge_color="gray"
    )

    plt.title(
        f"World Regional Hierarchy - {latest_year}",
        fontsize=16
    )

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "07_regional_hierarchy.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned dataset...")
    df = load_data()

    print("Building regional hierarchy...")
    graph, latest_year = build_regional_graph(df)

    print(f"Graph nodes: {graph.number_of_nodes()}")
    print(f"Graph edges: {graph.number_of_edges()}")

    print("Drawing regional hierarchy...")
    draw_regional_graph(graph, latest_year)

    print("\nNetworkX analysis completed successfully.")


if __name__ == "__main__":
    main()
